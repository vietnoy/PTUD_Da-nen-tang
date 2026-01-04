import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../providers/shopping_provider.dart';
import '../../providers/food_provider.dart';
import '../../models/shopping_task.dart';

class ShoppingListDetailsScreen extends StatefulWidget {
  final int listId;

  const ShoppingListDetailsScreen({super.key, required this.listId});

  @override
  State<ShoppingListDetailsScreen> createState() => _ShoppingListDetailsScreenState();
}

class _ShoppingListDetailsScreenState extends State<ShoppingListDetailsScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final shoppingProvider = Provider.of<ShoppingProvider>(context, listen: false);
      shoppingProvider.loadShoppingListDetails(widget.listId);
    });
  }

  Future<void> _showAddTaskDialog() async {
    final foodProvider = Provider.of<FoodProvider>(context, listen: false);
    await foodProvider.loadFoods();
    await foodProvider.loadUnits();

    final formKey = GlobalKey<FormState>();
    int? selectedFoodId;
    final quantityController = TextEditingController();
    int? selectedUnitId;
    final noteController = TextEditingController();
    final estimatedCostController = TextEditingController();
    String priority = 'medium';

    if (!mounted) return;

    final result = await showDialog<bool>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: const Text('Add Task'),
          content: SingleChildScrollView(
            child: Form(
              key: formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  DropdownButtonFormField<int>(
                    decoration: const InputDecoration(
                      labelText: 'Food Item *',
                      border: OutlineInputBorder(),
                    ),
                    value: selectedFoodId,
                    items: foodProvider.foods.map((food) {
                      return DropdownMenuItem<int>(
                        value: food.id,
                        child: Text(food.name),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedFoodId = value;
                      });
                    },
                    validator: (value) {
                      if (value == null) {
                        return 'Please select a food item';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: quantityController,
                    decoration: const InputDecoration(
                      labelText: 'Quantity *',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter quantity';
                      }
                      if (double.tryParse(value) == null) {
                        return 'Please enter a valid number';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<int>(
                    decoration: const InputDecoration(
                      labelText: 'Unit',
                      border: OutlineInputBorder(),
                    ),
                    value: selectedUnitId,
                    items: foodProvider.units.map((unit) {
                      return DropdownMenuItem<int>(
                        value: unit['id'] as int,
                        child: Text(unit['name'] ?? ''),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedUnitId = value;
                      });
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: estimatedCostController,
                    decoration: const InputDecoration(
                      labelText: 'Estimated Cost',
                      border: OutlineInputBorder(),
                      prefixText: '\$ ',
                    ),
                    keyboardType: TextInputType.number,
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    decoration: const InputDecoration(
                      labelText: 'Priority',
                      border: OutlineInputBorder(),
                    ),
                    value: priority,
                    items: const [
                      DropdownMenuItem(value: 'low', child: Text('Low')),
                      DropdownMenuItem(value: 'medium', child: Text('Medium')),
                      DropdownMenuItem(value: 'high', child: Text('High')),
                    ],
                    onChanged: (value) {
                      setState(() {
                        priority = value!;
                      });
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: noteController,
                    maxLines: 2,
                    decoration: const InputDecoration(
                      labelText: 'Note',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () async {
                if (formKey.currentState!.validate()) {
                  Navigator.pop(context, true);

                  final shoppingProvider = Provider.of<ShoppingProvider>(context, listen: false);
                  final success = await shoppingProvider.addShoppingTasks(
                    listId: widget.listId,
                    tasks: [
                      {
                        'foodId': selectedFoodId,
                        'quantity': quantityController.text,
                        'unitId': selectedUnitId,
                        'note': noteController.text.isEmpty ? null : noteController.text,
                        'estimatedCost': estimatedCostController.text.isEmpty ? null : estimatedCostController.text,
                        'priority': priority,
                      }
                    ],
                  );

                  if (mounted) {
                    if (success) {
                      await shoppingProvider.loadShoppingListDetails(widget.listId);
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Task added successfully'),
                          backgroundColor: Colors.green,
                        ),
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(shoppingProvider.errorMessage ?? 'Failed to add task'),
                          backgroundColor: Colors.red,
                        ),
                      );
                    }
                  }
                }
              },
              child: const Text('Add'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _toggleTaskDone(ShoppingTask task) async {
    final shoppingProvider = Provider.of<ShoppingProvider>(context, listen: false);
    await shoppingProvider.updateShoppingTask(
      taskId: task.id,
      listId: widget.listId,
      isDone: !task.isDone,
    );
    await shoppingProvider.loadShoppingListDetails(widget.listId);
  }

  Future<void> _deleteTask(ShoppingTask task) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Task'),
        content: Text('Are you sure you want to delete "${task.foodName}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirmed == true && mounted) {
      final shoppingProvider = Provider.of<ShoppingProvider>(context, listen: false);
      final success = await shoppingProvider.deleteShoppingTask(task.id, widget.listId);

      if (mounted) {
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Task deleted successfully'),
              backgroundColor: Colors.green,
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(shoppingProvider.errorMessage ?? 'Failed to delete task'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Future<void> _deleteList() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Shopping List'),
        content: const Text('Are you sure you want to delete this entire shopping list?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirmed == true && mounted) {
      final shoppingProvider = Provider.of<ShoppingProvider>(context, listen: false);
      final success = await shoppingProvider.deleteShoppingList(widget.listId);

      if (mounted) {
        if (success) {
          Navigator.pop(context, true);
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Shopping list deleted successfully'),
              backgroundColor: Colors.green,
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(shoppingProvider.errorMessage ?? 'Failed to delete list'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Color _getPriorityColor(String priority) {
    switch (priority) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
        return Colors.blue;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final shoppingProvider = Provider.of<ShoppingProvider>(context);
    final tasks = shoppingProvider.getTasksForList(widget.listId);
    final shoppingList = shoppingProvider.shoppingLists
        .firstWhere((list) => list.id == widget.listId, orElse: () => shoppingProvider.shoppingLists.first);

    final completedTasks = tasks.where((task) => task.isDone).length;
    final totalTasks = tasks.length;
    final totalEstimatedCost = tasks.fold<double>(
      0.0,
      (sum, task) => sum + (double.tryParse(task.estimatedCost ?? '0') ?? 0),
    );

    return Scaffold(
      appBar: AppBar(
        title: Text(shoppingList.name),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete, color: Colors.red),
            onPressed: _deleteList,
          ),
        ],
      ),
      body: shoppingProvider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  color: Colors.grey[100],
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Progress: $completedTasks/$totalTasks tasks',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            'Est. Total: \$${totalEstimatedCost.toStringAsFixed(2)}',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.green,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      LinearProgressIndicator(
                        value: totalTasks > 0 ? completedTasks / totalTasks : 0,
                        backgroundColor: Colors.grey[300],
                        valueColor: const AlwaysStoppedAnimation<Color>(Colors.green),
                      ),
                      if (shoppingList.description != null) ...[
                        const SizedBox(height: 12),
                        Text(
                          shoppingList.description!,
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[700],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                Expanded(
                  child: tasks.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.checklist,
                                size: 80,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No tasks in this list',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                              const SizedBox(height: 8),
                              ElevatedButton.icon(
                                onPressed: _showAddTaskDialog,
                                icon: const Icon(Icons.add),
                                label: const Text('Add First Task'),
                              ),
                            ],
                          ),
                        )
                      : RefreshIndicator(
                          onRefresh: () => shoppingProvider.loadShoppingListDetails(widget.listId),
                          child: ListView.builder(
                            itemCount: tasks.length,
                            itemBuilder: (context, index) {
                              final task = tasks[index];
                              return Card(
                                margin: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                child: ListTile(
                                  leading: Checkbox(
                                    value: task.isDone,
                                    onChanged: (_) => _toggleTaskDone(task),
                                    activeColor: Colors.green,
                                  ),
                                  title: Text(
                                    task.foodName,
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      decoration: task.isDone
                                          ? TextDecoration.lineThrough
                                          : null,
                                    ),
                                  ),
                                  subtitle: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const SizedBox(height: 4),
                                      Text('Quantity: ${task.quantity} ${task.unitName ?? ''}'),
                                      if (task.estimatedCost != null)
                                        Text('Est. Cost: \$${task.estimatedCost}'),
                                      Row(
                                        children: [
                                          Container(
                                            padding: const EdgeInsets.symmetric(
                                              horizontal: 6,
                                              vertical: 2,
                                            ),
                                            decoration: BoxDecoration(
                                              color: _getPriorityColor(task.priority)
                                                  .withOpacity(0.2),
                                              borderRadius: BorderRadius.circular(8),
                                            ),
                                            child: Text(
                                              task.priority.toUpperCase(),
                                              style: TextStyle(
                                                fontSize: 10,
                                                color: _getPriorityColor(task.priority),
                                                fontWeight: FontWeight.bold,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                      if (task.note != null && task.note!.isNotEmpty)
                                        Padding(
                                          padding: const EdgeInsets.only(top: 4),
                                          child: Text(
                                            task.note!,
                                            style: TextStyle(
                                              fontSize: 12,
                                              fontStyle: FontStyle.italic,
                                              color: Colors.grey[600],
                                            ),
                                          ),
                                        ),
                                    ],
                                  ),
                                  trailing: IconButton(
                                    icon: const Icon(Icons.delete, color: Colors.red),
                                    onPressed: () => _deleteTask(task),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                ),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddTaskDialog,
        child: const Icon(Icons.add),
      ),
    );
  }
}
