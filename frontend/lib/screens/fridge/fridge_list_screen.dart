import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/fridge_provider.dart';
import '../../models/fridge_item.dart';
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

  Color _getExpiryColor(FridgeItem item) {
    if (item.isExpired) return Colors.red;
    if (item.isExpiringSoon) return Colors.orange;
    return Colors.green;
  }

  String _getExpiryText(FridgeItem item) {
    if (item.isExpired) {
      return 'Expired ${item.daysUntilExpiry.abs()} days ago';
    } else if (item.daysUntilExpiry == 0) {
      return 'Expires today';
    } else if (item.daysUntilExpiry == 1) {
      return 'Expires tomorrow';
    } else {
      return 'Expires in ${item.daysUntilExpiry} days';
    }
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
                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: _getExpiryColor(item).withOpacity(0.2),
                            child: Icon(
                              Icons.fastfood,
                              color: _getExpiryColor(item),
                            ),
                          ),
                          title: Text(
                            item.foodName,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 4),
                              Text(
                                'Quantity: ${item.quantity} ${item.unitName ?? ''}',
                              ),
                              Text(
                                _getExpiryText(item),
                                style: TextStyle(
                                  color: _getExpiryColor(item),
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              if (item.location != null)
                                Text(
                                  'Location: ${item.location}',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                            ],
                          ),
                          trailing: PopupMenuButton(
                            itemBuilder: (context) => [
                              const PopupMenuItem(
                                value: 'edit',
                                child: Row(
                                  children: [
                                    Icon(Icons.edit),
                                    SizedBox(width: 8),
                                    Text('Edit'),
                                  ],
                                ),
                              ),
                              const PopupMenuItem(
                                value: 'delete',
                                child: Row(
                                  children: [
                                    Icon(Icons.delete, color: Colors.red),
                                    SizedBox(width: 8),
                                    Text('Delete', style: TextStyle(color: Colors.red)),
                                  ],
                                ),
                              ),
                            ],
                            onSelected: (value) async {
                              if (value == 'edit') {
                                final result = await Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => EditFridgeItemScreen(item: item),
                                  ),
                                );
                                if (result == true && mounted) {
                                  Provider.of<FridgeProvider>(context, listen: false).loadFridgeItems();
                                }
                              } else if (value == 'delete') {
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
                              }
                            },
                          ),
                        ),
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
