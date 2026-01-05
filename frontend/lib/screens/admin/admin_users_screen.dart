import 'package:flutter/material.dart';
import '../../services/admin_service.dart';

class AdminUsersScreen extends StatefulWidget {
  const AdminUsersScreen({super.key});

  @override
  State<AdminUsersScreen> createState() => _AdminUsersScreenState();
}

class _AdminUsersScreenState extends State<AdminUsersScreen> {
  final AdminService _adminService = AdminService();
  List<dynamic> _users = [];
  int _total = 0;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadUsers();
  }

  Future<void> _loadUsers() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final result = await _adminService.getAllUsers();
      setState(() {
        _users = result['users'] ?? [];
        _total = result['total'] ?? 0;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Lỗi tải danh sách users: $e')),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showUserDialog({Map<String, dynamic>? user}) {
    final isEdit = user != null;
    final formKey = GlobalKey<FormState>();
    final emailController = TextEditingController(text: user?['email'] ?? '');
    final nameController = TextEditingController(text: user?['name'] ?? '');
    final usernameController = TextEditingController(text: user?['username'] ?? '');
    final passwordController = TextEditingController();
    bool isActivated = user?['is_activated'] ?? true;
    bool isVerified = user?['is_verified'] ?? false;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: Text(isEdit ? 'Chỉnh sửa User' : 'Thêm User mới'),
          content: SingleChildScrollView(
            child: Form(
              key: formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextFormField(
                    controller: emailController,
                    decoration: const InputDecoration(labelText: 'Email'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Vui lòng nhập email';
                      }
                      if (!value.contains('@')) {
                        return 'Email không hợp lệ';
                      }
                      return null;
                    },
                  ),
                  TextFormField(
                    controller: nameController,
                    decoration: const InputDecoration(labelText: 'Tên'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Vui lòng nhập tên';
                      }
                      return null;
                    },
                  ),
                  TextFormField(
                    controller: usernameController,
                    decoration: const InputDecoration(labelText: 'Username'),
                  ),
                  if (!isEdit)
                    TextFormField(
                      controller: passwordController,
                      decoration: const InputDecoration(labelText: 'Password'),
                      obscureText: true,
                      validator: (value) {
                        if (!isEdit && (value == null || value.isEmpty)) {
                          return 'Vui lòng nhập password';
                        }
                        return null;
                      },
                    ),
                  if (isEdit)
                    TextFormField(
                      controller: passwordController,
                      decoration: const InputDecoration(
                        labelText: 'Password mới (để trống nếu không đổi)',
                      ),
                      obscureText: true,
                    ),
                  const SizedBox(height: 16),
                  SwitchListTile(
                    title: const Text('Activated'),
                    value: isActivated,
                    onChanged: (value) {
                      setDialogState(() {
                        isActivated = value;
                      });
                    },
                  ),
                  SwitchListTile(
                    title: const Text('Verified'),
                    value: isVerified,
                    onChanged: (value) {
                      setDialogState(() {
                        isVerified = value;
                      });
                    },
                  ),
                ],
              ),
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
                    final userData = {
                      'email': emailController.text,
                      'name': nameController.text,
                      'username': usernameController.text.isEmpty ? null : usernameController.text,
                      'is_activated': isActivated,
                      'is_verified': isVerified,
                    };

                    if (passwordController.text.isNotEmpty) {
                      userData['password'] = passwordController.text;
                    }

                    if (isEdit) {
                      await _adminService.updateUser(user['id'], userData);
                    } else {
                      await _adminService.createUser(userData);
                    }

                    if (context.mounted) {
                      Navigator.of(context).pop();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(isEdit ? 'Cập nhật thành công' : 'Thêm thành công'),
                          backgroundColor: Colors.green,
                        ),
                      );
                      _loadUsers();
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
      ),
    );
  }

  void _deleteUser(int userId, String userName) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Xác nhận xóa'),
        content: Text('Bạn có chắc chắn muốn xóa user "$userName"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Hủy'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await _adminService.deleteUser(userId);
                if (context.mounted) {
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Xóa thành công'),
                      backgroundColor: Colors.green,
                    ),
                  );
                  _loadUsers();
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
              onRefresh: _loadUsers,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Tổng: $_total users',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        ElevatedButton.icon(
                          onPressed: () => _showUserDialog(),
                          icon: const Icon(Icons.add),
                          label: const Text('Thêm User'),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: _users.isEmpty
                        ? const Center(child: Text('Không có user nào'))
                        : ListView.builder(
                            itemCount: _users.length,
                            itemBuilder: (context, index) {
                              final user = _users[index];
                              return Card(
                                margin: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    child: Text(user['name'][0].toUpperCase()),
                                  ),
                                  title: Text(user['name']),
                                  subtitle: Text(
                                    '${user['email']}\n'
                                    'Username: ${user['username'] ?? 'N/A'}\n'
                                    'Activated: ${user['is_activated']}, '
                                    'Verified: ${user['is_verified']}',
                                  ),
                                  isThreeLine: true,
                                  trailing: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      IconButton(
                                        icon: const Icon(Icons.edit),
                                        onPressed: () => _showUserDialog(user: user),
                                        tooltip: 'Chỉnh sửa',
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        color: Colors.red,
                                        onPressed: () => _deleteUser(
                                          user['id'],
                                          user['name'],
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
