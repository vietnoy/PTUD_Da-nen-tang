import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/shopping_provider.dart';
import '../../models/shopping_list.dart';
import 'package:intl/intl.dart';
import 'shopping_list_details_screen.dart';

class ShoppingListsScreen extends StatefulWidget {
  const ShoppingListsScreen({super.key});

  @override
  State<ShoppingListsScreen> createState() => _ShoppingListsScreenState();
}

class _ShoppingListsScreenState extends State<ShoppingListsScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<ShoppingProvider>(context, listen: false).loadShoppingLists();
    });
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

  Color _getStatusColor(String status) {
    switch (status) {
      case 'pending':
        return Colors.orange;
      case 'inProgress':
        return Colors.blue;
      case 'completed':
        return Colors.green;
      case 'cancelled':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final shoppingProvider = Provider.of<ShoppingProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Shopping Lists'),
      ),
      body: shoppingProvider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : shoppingProvider.shoppingLists.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.shopping_cart,
                        size: 80,
                        color: Colors.grey[400],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No shopping lists',
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: () => shoppingProvider.loadShoppingLists(),
                  child: ListView.builder(
                    itemCount: shoppingProvider.shoppingLists.length,
                    itemBuilder: (context, index) {
                      final list = shoppingProvider.shoppingLists[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: _getPriorityColor(list.priority)
                                .withOpacity(0.2),
                            child: Icon(
                              Icons.shopping_basket,
                              color: _getPriorityColor(list.priority),
                            ),
                          ),
                          title: Text(
                            list.name,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(
                                      horizontal: 8,
                                      vertical: 2,
                                    ),
                                    decoration: BoxDecoration(
                                      color: _getStatusColor(list.status)
                                          .withOpacity(0.2),
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                    child: Text(
                                      list.status.toUpperCase(),
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: _getStatusColor(list.status),
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    'Total: \$${list.totalCost}',
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                ],
                              ),
                              if (list.dueDate != null)
                                Padding(
                                  padding: const EdgeInsets.only(top: 4),
                                  child: Text(
                                    'Due: ${DateFormat('MMM dd, yyyy').format(list.dueDate!)}',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.grey[600],
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          trailing: const Icon(Icons.chevron_right),
                          onTap: () async {
                            final result = await Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => ShoppingListDetailsScreen(listId: list.id),
                              ),
                            );
                            if (result == true && mounted) {
                              Provider.of<ShoppingProvider>(context, listen: false).loadShoppingLists();
                            }
                          },
                        ),
                      );
                    },
                  ),
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/shopping/create');
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
