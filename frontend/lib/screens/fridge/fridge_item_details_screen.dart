import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../providers/fridge_provider.dart';

class FridgeItemDetailsScreen extends StatelessWidget {
  final String itemId;

  const FridgeItemDetailsScreen({
    super.key,
    required this.itemId,
  });

  @override
  Widget build(BuildContext context) {
    final fridgeProvider = context.watch<FridgeProvider>();
    final item = fridgeProvider.items.firstWhere(
      (item) => item.id == itemId,
      orElse: () => throw Exception('Item not found'),
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('Item Details'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: () async {
              final confirm = await showDialog<bool>(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Delete Item'),
                  content: const Text('Are you sure you want to delete this item?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context, false),
                      child: const Text('Cancel'),
                    ),
                    TextButton(
                      onPressed: () => Navigator.pop(context, true),
                      child: const Text('Delete', style: TextStyle(color: Colors.red)),
                    ),
                  ],
                ),
              );

              if (confirm == true && context.mounted) {
                final success = await fridgeProvider.deleteFridgeItem(itemId);
                if (context.mounted) {
                  if (success) {
                    context.pop();
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(fridgeProvider.error ?? 'Failed to delete item'),
                        backgroundColor: Colors.red,
                      ),
                    );
                  }
                }
              }
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (item.foodImageUrl != null)
              Image.network(
                item.foodImageUrl!,
                height: 200,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    height: 200,
                    color: Colors.grey.shade200,
                    child: const Icon(Icons.fastfood, size: 80),
                  );
                },
              )
            else
              Container(
                height: 200,
                color: Colors.grey.shade200,
                child: const Icon(Icons.fastfood, size: 80),
              ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.foodName,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  _buildDetailRow('Quantity', '${item.quantity} ${item.unitName ?? 'units'}'),
                  _buildDetailRow('Use Within Date', DateFormat('MMM d, y').format(item.useWithinDate)),
                  _buildDetailRow('Days Until Expiry', '${item.daysUntilExpiry} days'),
                  if (item.location != null)
                    _buildDetailRow('Location', item.location!),
                  if (item.cost != null)
                    _buildDetailRow('Cost', '\$${item.cost!.toStringAsFixed(2)}'),
                  _buildDetailRow('Status', item.isOpened ? 'Opened' : 'Unopened'),
                  _buildDetailRow('Added', DateFormat('MMM d, y').format(item.createdAt)),
                  const SizedBox(height: 24),
                  SwitchListTile(
                    title: const Text('Mark as Opened'),
                    value: item.isOpened,
                    onChanged: (value) async {
                      await fridgeProvider.updateFridgeItem(
                        id: itemId,
                        isOpened: value,
                      );
                    },
                    activeColor: const Color(0xFF4CAF50),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 140,
            child: Text(
              label,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade600,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
