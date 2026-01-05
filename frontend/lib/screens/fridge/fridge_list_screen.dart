import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/fridge_provider.dart';
import '../../models/fridge_item.dart';
import '../../widgets/fridge_item_card.dart';
import 'package:intl/intl.dart';
import 'edit_fridge_item_screen.dart';

class FridgeListScreen extends StatefulWidget {
  const FridgeListScreen({super.key});

  @override
  State<FridgeListScreen> createState() => _FridgeListScreenState();
}

class _FridgeListScreenState extends State<FridgeListScreen> {
  String? _selectedLocation;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<FridgeProvider>(context, listen: false).loadFridgeItems();
    });
  }

  @override
  Widget build(BuildContext context) {
    final fridgeProvider = Provider.of<FridgeProvider>(context);
    
    final filteredItems = _selectedLocation == null
        ? fridgeProvider.fridgeItems
        : fridgeProvider.getItemsByLocation(_selectedLocation);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Fridge'),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.filter_list),
            onSelected: (value) {
              setState(() {
                _selectedLocation = value == 'all' ? null : value;
              });
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'all',
                child: Text('All Locations'),
              ),
              const PopupMenuItem(
                value: 'fridge',
                child: Text('Fridge'),
              ),
              const PopupMenuItem(
                value: 'freezer',
                child: Text('Freezer'),
              ),
              const PopupMenuItem(
                value: 'pantry',
                child: Text('Pantry'),
              ),
            ],
          ),
        ],
      ),
      body: fridgeProvider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : filteredItems.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.kitchen,
                        size: 80,
                        color: Colors.grey[400],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No items in fridge',
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: () => fridgeProvider.loadFridgeItems(),
                  child: ListView.builder(
                    itemCount: filteredItems.length,
                    itemBuilder: (context, index) {
                      final item = filteredItems[index];
                      return FridgeItemCard(
                        item: item,
                        onTap: () async {
                          // Show options bottom sheet
                          showModalBottomSheet(
                            context: context,
                            builder: (context) => SafeArea(
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  ListTile(
                                    leading: const Icon(Icons.edit),
                                    title: const Text('Edit'),
                                    onTap: () async {
                                      Navigator.pop(context);
                                      final result = await Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) => EditFridgeItemScreen(item: item),
                                        ),
                                      );
                                      if (result == true && mounted) {
                                        Provider.of<FridgeProvider>(context, listen: false).loadFridgeItems();
                                      }
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(Icons.delete, color: Colors.red),
                                    title: const Text('Delete', style: TextStyle(color: Colors.red)),
                                    onTap: () async {
                                      Navigator.pop(context);
                                      final confirm = await showDialog<bool>(
                                        context: context,
                                        builder: (context) => AlertDialog(
                                          title: const Text('Delete Item'),
                                          content: Text('Delete ${item.foodName}?'),
                                          actions: [
                                            TextButton(
                                              onPressed: () => Navigator.pop(context, false),
                                              child: const Text('Cancel'),
                                            ),
                                            TextButton(
                                              onPressed: () => Navigator.pop(context, true),
                                              child: const Text(
                                                'Delete',
                                                style: TextStyle(color: Colors.red),
                                              ),
                                            ),
                                          ],
                                        ),
                                      );

                                      if (confirm == true && mounted) {
                                        await fridgeProvider.deleteFridgeItem(item.id);
                                      }
                                    },
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/fridge/add');
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
