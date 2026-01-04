import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../providers/fridge_provider.dart';
import '../../providers/food_provider.dart';
import '../../models/fridge_item.dart';

class EditFridgeItemScreen extends StatefulWidget {
  final FridgeItem item;

  const EditFridgeItemScreen({super.key, required this.item});

  @override
  State<EditFridgeItemScreen> createState() => _EditFridgeItemScreenState();
}

class _EditFridgeItemScreenState extends State<EditFridgeItemScreen> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _quantityController;
  late final TextEditingController _noteController;
  late final TextEditingController _costController;
  late DateTime? _purchaseDate;
  late DateTime _useWithinDate;
  late int? _selectedUnitId;
  late String? _selectedLocation;
  late bool _isOpened;

  final List<String> _locations = ['fridge', 'freezer', 'pantry'];

  @override
  void initState() {
    super.initState();
    _quantityController = TextEditingController(text: widget.item.quantity);
    _noteController = TextEditingController(text: widget.item.note ?? '');
    _costController = TextEditingController(text: widget.item.cost ?? '');
    _purchaseDate = widget.item.purchaseDate;
    _useWithinDate = widget.item.useWithinDate;
    _selectedUnitId = widget.item.unitId;
    _selectedLocation = widget.item.location;
    _isOpened = widget.item.isOpened;

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final foodProvider = Provider.of<FoodProvider>(context, listen: false);
      foodProvider.loadUnits();
    });
  }

  @override
  void dispose() {
    _quantityController.dispose();
    _noteController.dispose();
    _costController.dispose();
    super.dispose();
  }

  Future<void> _selectPurchaseDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _purchaseDate ?? DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() {
        _purchaseDate = picked;
      });
    }
  }

  Future<void> _selectUseWithinDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _useWithinDate,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null) {
      setState(() {
        _useWithinDate = picked;
      });
    }
  }

  Future<void> _handleSave() async {
    if (_formKey.currentState!.validate()) {
      final fridgeProvider = Provider.of<FridgeProvider>(context, listen: false);

      final success = await fridgeProvider.updateFridgeItem(
        fridgeItemId: widget.item.id,
        quantity: _quantityController.text.trim(),
        unitId: _selectedUnitId,
        note: _noteController.text.trim().isEmpty ? null : _noteController.text.trim(),
        purchaseDate: _purchaseDate,
        useWithinDate: _useWithinDate,
        location: _selectedLocation,
        isOpened: _isOpened,
        openedAt: _isOpened ? DateTime.now() : null,
        cost: _costController.text.trim().isEmpty ? null : _costController.text.trim(),
      );

      if (!mounted) return;

      if (success) {
        Navigator.pop(context, true);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Fridge item updated successfully'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(fridgeProvider.errorMessage ?? 'Failed to update fridge item'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _handleDelete() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Fridge Item'),
        content: Text('Are you sure you want to delete "${widget.item.foodName}"?'),
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
      final fridgeProvider = Provider.of<FridgeProvider>(context, listen: false);
      final success = await fridgeProvider.deleteFridgeItem(widget.item.id);

      if (!mounted) return;

      if (success) {
        Navigator.pop(context, true);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Fridge item deleted successfully'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(fridgeProvider.errorMessage ?? 'Failed to delete fridge item'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final fridgeProvider = Provider.of<FridgeProvider>(context);
    final foodProvider = Provider.of<FoodProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Fridge Item'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete, color: Colors.red),
            onPressed: _handleDelete,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                widget.item.foodName,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 24),
              TextFormField(
                controller: _quantityController,
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
                items: _locations.map((location) {
                  return DropdownMenuItem<String>(
                    value: location,
                    child: Text(location[0].toUpperCase() + location.substring(1)),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedLocation = value;
                  });
                },
              ),
              const SizedBox(height: 16),
              InkWell(
                onTap: _selectPurchaseDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    labelText: 'Purchase Date',
                    border: OutlineInputBorder(),
                    suffixIcon: Icon(Icons.calendar_today),
                  ),
                  child: Text(
                    _purchaseDate != null
                        ? DateFormat('MMM dd, yyyy').format(_purchaseDate!)
                        : 'Not set',
                    style: TextStyle(
                      color: _purchaseDate != null ? Colors.black : Colors.grey,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              InkWell(
                onTap: _selectUseWithinDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    labelText: 'Use Within Date *',
                    border: OutlineInputBorder(),
                    suffixIcon: Icon(Icons.calendar_today),
                  ),
                  child: Text(
                    DateFormat('MMM dd, yyyy').format(_useWithinDate),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _costController,
                decoration: const InputDecoration(
                  labelText: 'Cost',
                  border: OutlineInputBorder(),
                  prefixText: '\$ ',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value != null && value.isNotEmpty) {
                    if (double.tryParse(value) == null) {
                      return 'Please enter a valid number';
                    }
                  }
                  return null;
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
              const SizedBox(height: 16),
              SwitchListTile(
                title: const Text('Is Opened'),
                subtitle: Text(_isOpened ? 'Package is opened' : 'Package is sealed'),
                value: _isOpened,
                onChanged: (value) {
                  setState(() {
                    _isOpened = value;
                  });
                },
                contentPadding: EdgeInsets.zero,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: fridgeProvider.isLoading ? null : _handleSave,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: fridgeProvider.isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Save Changes', style: TextStyle(fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
