import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/fridge_provider.dart';
import '../../providers/food_provider.dart';

class AddFridgeItemScreen extends StatefulWidget {
  const AddFridgeItemScreen({super.key});

  @override
  State<AddFridgeItemScreen> createState() => _AddFridgeItemScreenState();
}

class _AddFridgeItemScreenState extends State<AddFridgeItemScreen> {
  final _formKey = GlobalKey<FormState>();
  int? _selectedFoodId;
  final _quantityController = TextEditingController();
  int? _selectedUnitId;
  String? _selectedLocation = 'fridge';
  DateTime? _purchaseDate;
  DateTime _useWithinDate = DateTime.now().add(const Duration(days: 7));
  final _noteController = TextEditingController();
  bool _isOpened = false;
  DateTime? _openedAt;
  final _costController = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<FoodProvider>(context, listen: false).loadFoods();
      Provider.of<FoodProvider>(context, listen: false).loadUnits();
    });
  }

  @override
  void dispose() {
    _quantityController.dispose();
    _noteController.dispose();
    _costController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context, bool isUseWithin) async {
    final initialDate = isUseWithin ? _useWithinDate : (_purchaseDate ?? DateTime.now());
    
    final picked = await showDatePicker(
      context: context,
      initialDate: initialDate,
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),
    );

    if (picked != null) {
      setState(() {
        if (isUseWithin) {
          _useWithinDate = picked;
        } else {
          _purchaseDate = picked;
        }
      });
    }
  }

  Future<void> _handleSubmit() async {
    if (_formKey.currentState!.validate() && _selectedFoodId != null) {
      final fridgeProvider = Provider.of<FridgeProvider>(context, listen: false);

      final success = await fridgeProvider.createFridgeItem(
        foodId: _selectedFoodId!,
        quantity: _quantityController.text,
        unitId: _selectedUnitId,
        note: _noteController.text.isNotEmpty ? _noteController.text : null,
        purchaseDate: _purchaseDate,
        useWithinDate: _useWithinDate,
        location: _selectedLocation,
        isOpened: _isOpened,
        openedAt: _openedAt,
        cost: _costController.text.isNotEmpty ? _costController.text : null,
      );

      if (!mounted) return;

      if (success) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Fridge item added successfully'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(fridgeProvider.errorMessage ?? 'Failed to add item'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } else if (_selectedFoodId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select a food item'),
          backgroundColor: Colors.orange,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final foodProvider = Provider.of<FoodProvider>(context);
    final fridgeProvider = Provider.of<FridgeProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Fridge Item'),
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
                  labelText: 'Food Item *',
                  border: OutlineInputBorder(),
                ),
                value: _selectedFoodId,
                items: foodProvider.foods.map((food) {
                  return DropdownMenuItem(
                    value: food.id,
                    child: Text(food.name),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedFoodId = value;
                  });
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _quantityController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Quantity *',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter quantity';
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
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(
                  labelText: 'Location',
                  border: OutlineInputBorder(),
                ),
                value: _selectedLocation,
                items: const [
                  DropdownMenuItem(value: 'fridge', child: Text('Fridge')),
                  DropdownMenuItem(value: 'freezer', child: Text('Freezer')),
                  DropdownMenuItem(value: 'pantry', child: Text('Pantry')),
                ],
                onChanged: (value) {
                  setState(() {
                    _selectedLocation = value;
                  });
                },
              ),
              const SizedBox(height: 16),
              ListTile(
                title: const Text('Purchase Date'),
                subtitle: Text(_purchaseDate != null
                    ? '${_purchaseDate!.day}/${_purchaseDate!.month}/${_purchaseDate!.year}'
                    : 'Not set'),
                trailing: const Icon(Icons.calendar_today),
                onTap: () => _selectDate(context, false),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(color: Colors.grey[400]!),
                ),
              ),
              const SizedBox(height: 16),
              ListTile(
                title: const Text('Use Within Date *'),
                subtitle: Text(
                  '${_useWithinDate.day}/${_useWithinDate.month}/${_useWithinDate.year}',
                ),
                trailing: const Icon(Icons.calendar_today),
                onTap: () => _selectDate(context, true),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(color: Colors.grey[400]!),
                ),
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
              const SizedBox(height: 16),
              TextFormField(
                controller: _costController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Cost',
                  prefixText: '\$',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              SwitchListTile(
                title: const Text('Is Opened'),
                value: _isOpened,
                onChanged: (value) {
                  setState(() {
                    _isOpened = value;
                    if (value) {
                      _openedAt = DateTime.now();
                    } else {
                      _openedAt = null;
                    }
                  });
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: fridgeProvider.isLoading ? null : _handleSubmit,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: fridgeProvider.isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Add Item', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
