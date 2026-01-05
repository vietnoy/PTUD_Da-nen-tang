import 'package:flutter/material.dart';
import '../../services/admin_service.dart';

class AdminCategoriesScreen extends StatefulWidget {
  const AdminCategoriesScreen({super.key});

  @override
  State<AdminCategoriesScreen> createState() => _AdminCategoriesScreenState();
}

class _AdminCategoriesScreenState extends State<AdminCategoriesScreen> {
  final AdminService _adminService = AdminService();
  List<dynamic> _categories = [];
  int _total = 0;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  Future<void> _loadCategories() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final result = await _adminService.getAllCategories();
      setState(() {
        _categories = result['categories'] ?? [];
        _total = result['total'] ?? 0;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Lỗi tải danh sách categories: $e')),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showCategoryDialog({Map<String, dynamic>? category}) {
    final isEdit = category != null;
    final formKey = GlobalKey<FormState>();
    final nameController = TextEditingController(text: category?['name'] ?? '');
    final descriptionController = TextEditingController(
      text: category?['description'] ?? '',
    );

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(isEdit ? 'Chỉnh sửa Category' : 'Thêm Category mới'),
        content: Form(
          key: formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: nameController,
                decoration: const InputDecoration(labelText: 'Tên danh mục'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Vui lòng nhập tên danh mục';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: descriptionController,
                decoration: const InputDecoration(labelText: 'Mô tả'),
                maxLines: 3,
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Hủy'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (formKey.currentState!.validate()) {
                try {
                  final categoryData = {
                    'name': nameController.text,
                    'description': descriptionController.text.isEmpty
                        ? null
                        : descriptionController.text,
                  };

                  if (isEdit) {
                    await _adminService.updateCategory(
                      category['id'],
                      categoryData,
                    );
                  } else {
                    await _adminService.createCategory(categoryData);
                  }

                  if (context.mounted) {
                    Navigator.of(context).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(isEdit ? 'Cập nhật thành công' : 'Thêm thành công'),
                        backgroundColor: Colors.green,
                      ),
                    );
                    _loadCategories();
                  }
                } catch (e) {
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Lỗi: $e')),
                    );
                  }
                }
              }
            },
            child: Text(isEdit ? 'Cập nhật' : 'Thêm'),
          ),
        ],
      ),
    );
  }

  void _deleteCategory(int categoryId, String categoryName) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Xác nhận xóa'),
        content: Text('Bạn có chắc chắn muốn xóa danh mục "$categoryName"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Hủy'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await _adminService.deleteCategory(categoryId);
                if (context.mounted) {
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Xóa thành công'),
                      backgroundColor: Colors.green,
                    ),
                  );
                  _loadCategories();
                }
              } catch (e) {
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Lỗi: $e')),
                  );
                }
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('Xóa'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadCategories,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Tổng: $_total categories',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        ElevatedButton.icon(
                          onPressed: () => _showCategoryDialog(),
                          icon: const Icon(Icons.add),
                          label: const Text('Thêm Category'),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: _categories.isEmpty
                        ? const Center(child: Text('Không có category nào'))
                        : ListView.builder(
                            itemCount: _categories.length,
                            itemBuilder: (context, index) {
                              final category = _categories[index];
                              return Card(
                                margin: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    child: Text(category['name'][0].toUpperCase()),
                                  ),
                                  title: Text(category['name']),
                                  subtitle: Text(
                                    category['description'] ?? 'Không có mô tả',
                                  ),
                                  trailing: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      IconButton(
                                        icon: const Icon(Icons.edit),
                                        onPressed: () => _showCategoryDialog(
                                          category: category,
                                        ),
                                        tooltip: 'Chỉnh sửa',
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        color: Colors.red,
                                        onPressed: () => _deleteCategory(
                                          category['id'],
                                          category['name'],
                                        ),
                                        tooltip: 'Xóa',
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                  ),
                ],
              ),
            ),
    );
  }
}
