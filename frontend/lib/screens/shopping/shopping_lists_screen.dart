import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/shopping_provider.dart';
import '../../models/shopping_list.dart';
import '../../widgets/shopping_list_card.dart';
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
                      return ShoppingListCard(
                        list: list,
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
