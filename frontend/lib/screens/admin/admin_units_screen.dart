import 'package:flutter/material.dart';
import '../../services/admin_service.dart';

class AdminUnitsScreen extends StatefulWidget {
  const AdminUnitsScreen({super.key});

  @override
  State<AdminUnitsScreen> createState() => _AdminUnitsScreenState();
}

class _AdminUnitsScreenState extends State<AdminUnitsScreen> {
  final AdminService _adminService = AdminService();
  List<dynamic> _units = [];
  int _total = 0;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadUnits();
  }

  Future<void> _loadUnits() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final result = await _adminService.getAllUnits();
      setState(() {
        _units = result['units'] ?? [];
        _total = result['total'] ?? 0;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Lỗi tải danh sách units: $e')),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showUnitDialog({Map<String, dynamic>? unit}) {
    final isEdit = unit != null;
    final formKey = GlobalKey<FormState>();
    final nameController = TextEditingController(text: unit?['name'] ?? '');
    String selectedType = unit?['type'] ?? 'weight';
    final convertToBaseController = TextEditingController(
      text: unit?['convert_to_base']?.toString() ?? '1.0',
    );
    bool isBaseUnit = unit?['is_base_unit'] ?? false;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: Text(isEdit ? 'Chỉnh sửa Unit' : 'Thêm Unit mới'),
          content: SingleChildScrollView(
            child: Form(
              key: formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextFormField(
                    controller: nameController,
                    decoration: const InputDecoration(labelText: 'Tên đơn vị'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Vui lòng nhập tên đơn vị';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    initialValue: selectedType,
                    decoration: const InputDecoration(labelText: 'Loại'),
                    items: const [
                      DropdownMenuItem(value: 'weight', child: Text('Weight')),
                      DropdownMenuItem(value: 'volume', child: Text('Volume')),
                      DropdownMenuItem(value: 'count', child: Text('Count')),
                      DropdownMenuItem(value: 'length', child: Text('Length')),
                    ],
                    onChanged: (value) {
                      setDialogState(() {
                        selectedType = value!;
                      });
                    },
                  ),
                  TextFormField(
                    controller: convertToBaseController,
                    decoration: const InputDecoration(
                      labelText: 'Convert to base',
                      helperText: 'Hệ số chuyển đổi sang đơn vị cơ bản',
                    ),
                    keyboardType: const TextInputType.numberWithOptions(decimal: true),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Vui lòng nhập hệ số chuyển đổi';
                      }
                      if (double.tryParse(value) == null) {
                        return 'Vui lòng nhập số hợp lệ';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  SwitchListTile(
                    title: const Text('Is Base Unit'),
                    subtitle: const Text('Đây có phải đơn vị cơ bản?'),
                    value: isBaseUnit,
                    onChanged: (value) {
                      setDialogState(() {
                        isBaseUnit = value;
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
                    final unitData = {
                      'name': nameController.text,
                      'type': selectedType,
                      'convert_to_base': convertToBaseController.text,
                      'is_base_unit': isBaseUnit,
                    };

                    if (isEdit) {
                      await _adminService.updateUnit(unit['id'], unitData);
                    } else {
                      await _adminService.createUnit(unitData);
                    }

                    if (context.mounted) {
                      Navigator.of(context).pop();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(isEdit ? 'Cập nhật thành công' : 'Thêm thành công'),
                          backgroundColor: Colors.green,
                        ),
                      );
                      _loadUnits();
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

  void _deleteUnit(int unitId, String unitName) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Xác nhận xóa'),
        content: Text('Bạn có chắc chắn muốn xóa đơn vị "$unitName"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Hủy'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await _adminService.deleteUnit(unitId);
                if (context.mounted) {
                  Navigator.of(context).pop();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Xóa thành công'),
                      backgroundColor: Colors.green,
                    ),
                  );
                  _loadUnits();
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
              onRefresh: _loadUnits,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Tổng: $_total units',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        ElevatedButton.icon(
                          onPressed: () => _showUnitDialog(),
                          icon: const Icon(Icons.add),
                          label: const Text('Thêm Unit'),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: _units.isEmpty
                        ? const Center(child: Text('Không có unit nào'))
                        : ListView.builder(
                            itemCount: _units.length,
                            itemBuilder: (context, index) {
                              final unit = _units[index];
                              return Card(
                                margin: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    child: Text(unit['name'][0].toUpperCase()),
                                  ),
                                  title: Text(unit['name']),
                                  subtitle: Text(
                                    'Type: ${unit['type']}\n'
                                    'Convert to base: ${unit['convert_to_base']}\n'
                                    'Base unit: ${unit['is_base_unit']}',
                                  ),
                                  isThreeLine: true,
                                  trailing: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      IconButton(
                                        icon: const Icon(Icons.edit),
                                        onPressed: () => _showUnitDialog(unit: unit),
                                        tooltip: 'Chỉnh sửa',
                                      ),
                                      IconButton(
                                        icon: const Icon(Icons.delete),
                                        color: Colors.red,
                                        onPressed: () => _deleteUnit(
                                          unit['id'],
                                          unit['name'],
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
