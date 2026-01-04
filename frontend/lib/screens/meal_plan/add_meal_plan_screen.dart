import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/meal_plan_provider.dart';
import '../../providers/food_provider.dart';

class AddMealPlanScreen extends StatefulWidget {
  final DateTime? selectedDate;
  
  const AddMealPlanScreen({super.key, this.selectedDate});

  @override
  State<AddMealPlanScreen> createState() => _AddMealPlanScreenState();
}

class _AddMealPlanScreenState extends State<AddMealPlanScreen> {
  final _formKey = GlobalKey<FormState>();
  int? _selectedFoodId;
  String _mealType = 'breakfast';
  late DateTime _mealDate;
  final _servingSizeController = TextEditingController();
  int? _selectedUnitId;
  final _noteController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _mealDate = widget.selectedDate ?? DateTime.now();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final foodProvider = Provider.of<FoodProvider>(context, listen: false);
      foodProvider.loadFoods();
      foodProvider.loadUnits();
    });
  }

  @override
  void dispose() {
    _servingSizeController.dispose();
    _noteController.dispose();
    super.dispose();
  }

  Future<void> _selectDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _mealDate,
      firstDate: DateTime.now().subtract(const Duration(days: 365)),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null) {
      setState(() {
        _mealDate = picked;
      });
    }
  }

  Future<void> _handleSave() async {
    if (_formKey.currentState!.validate() && _selectedFoodId != null) {
      final mealPlanProvider = Provider.of<MealPlanProvider>(context, listen: false);

      final success = await mealPlanProvider.createMealPlan(
        foodId: _selectedFoodId!,
        mealType: _mealType,
        mealDate: _mealDate,
        servingSize: _servingSizeController.text.isNotEmpty ? _servingSizeController.text : null,
        unitId: _selectedUnitId,
        note: _noteController.text.isNotEmpty ? _noteController.text : null,
      );

      if (!mounted) return;

      if (success) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Meal plan added'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(mealPlanProvider.errorMessage ?? 'Failed to add meal'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final foodProvider = Provider.of<FoodProvider>(context);
    final mealPlanProvider = Provider.of<MealPlanProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Meal Plan'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              DropdownButtonFormField<int>(
                decoration: const InputDecoration(
                  labelText: 'Food *',
                  border: OutlineInputBorder(),
                ),
                value: _selectedFoodId,
                items: foodProvider.foods.map((food) {
                  return DropdownMenuItem<int>(
                    value: food.id,
                    child: Text(food.name),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedFoodId = value;
                  });
                },
                validator: (value) {
                  if (value == null) {
                    return 'Please select a food';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: _mealType,
                decoration: const InputDecoration(
                  labelText: 'Meal Type',
                  border: OutlineInputBorder(),
                ),
                items: const [
                  DropdownMenuItem(value: 'breakfast', child: Text('Breakfast')),
                  DropdownMenuItem(value: 'lunch', child: Text('Lunch')),
                  DropdownMenuItem(value: 'dinner', child: Text('Dinner')),
                  DropdownMenuItem(value: 'snack', child: Text('Snack')),
                ],
                onChanged: (value) {
                  setState(() {
                    _mealType = value!;
                  });
                },
              ),
              const SizedBox(height: 16),
              ListTile(
                title: const Text('Meal Date'),
                subtitle: Text('${_mealDate.day}/${_mealDate.month}/${_mealDate.year}'),
                trailing: const Icon(Icons.calendar_today),
                onTap: _selectDate,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(color: Colors.grey[400]!),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _servingSizeController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Serving Size',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<int>(
                decoration: const InputDecoration(
                  labelText: 'Unit',
                  border: OutlineInputBorder(),
                ),
                value: _selectedUnitId,
                items: foodProvider.units.map((unit) {
                  return DropdownMenuItem<int>(
                    value: unit['id'] as int,
                    child: Text(unit['name'] ?? ''),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedUnitId = value;
                  });
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _noteController,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'Note',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: mealPlanProvider.isLoading ? null : _handleSave,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: mealPlanProvider.isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Add Meal', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
