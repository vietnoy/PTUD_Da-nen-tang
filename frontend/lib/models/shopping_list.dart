class ShoppingList {
  final int id;
  final String name;
  final String? description;
  final int groupId;
  final int? assignToId;
  final String? assignToUsername;
  final DateTime? dueDate;
  final String status;
  final String priority;
  final String? budget;
  final String totalCost;
  final int createdBy;
  final String? createdByUsername;
  final DateTime createdAt;
  final DateTime updatedAt;

  ShoppingList({
    required this.id,
    required this.name,
    this.description,
    required this.groupId,
    this.assignToId,
    this.assignToUsername,
    this.dueDate,
    required this.status,
    required this.priority,
    this.budget,
    required this.totalCost,
    required this.createdBy,
    this.createdByUsername,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ShoppingList.fromJson(Map<String, dynamic> json) {
    return ShoppingList(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      groupId: json['groupId'],
      assignToId: json['assignToId'],
      assignToUsername: json['assignToUsername'],
      dueDate: json['dueDate'] != null ? DateTime.parse(json['dueDate']) : null,
      status: json['status'],
      priority: json['priority'],
      budget: json['budget']?.toString(),
      totalCost: json['totalCost'].toString(),
      createdBy: json['createdBy'],
      createdByUsername: json['createdByUsername'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }

  // Computed properties
  bool get isOverdue {
    if (dueDate == null) return false;
    return DateTime.now().isAfter(dueDate!) && status != 'completed';
  }

  String? get assignToName => assignToUsername;
}
