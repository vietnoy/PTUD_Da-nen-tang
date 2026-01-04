class ShoppingTask {
  final int id;
  final int listId;
  final int foodId;
  final String foodName;
  final String quantity;
  final int? unitId;
  final String? unitName;
  final String? note;
  final bool isDone;
  final String? estimatedCost;
  final String? actualCost;
  final String priority;
  final DateTime createdAt;
  final DateTime updatedAt;

  ShoppingTask({
    required this.id,
    required this.listId,
    required this.foodId,
    required this.foodName,
    required this.quantity,
    this.unitId,
    this.unitName,
    this.note,
    required this.isDone,
    this.estimatedCost,
    this.actualCost,
    required this.priority,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ShoppingTask.fromJson(Map<String, dynamic> json) {
    return ShoppingTask(
      id: json['id'],
      listId: json['listId'],
      foodId: json['foodId'],
      foodName: json['foodName'],
      quantity: json['quantity'].toString(),
      unitId: json['unitId'],
      unitName: json['unitName'],
      note: json['note'],
      isDone: json['isDone'],
      estimatedCost: json['estimatedCost']?.toString(),
      actualCost: json['actualCost']?.toString(),
      priority: json['priority'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}
