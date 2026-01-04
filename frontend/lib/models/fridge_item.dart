class FridgeItem {
  final int id;
  final int foodId;
  final String foodName;
  final int groupId;
  final String quantity;
  final int? unitId;
  final String? unitName;
  final String? note;
  final DateTime? purchaseDate;
  final DateTime useWithinDate;
  final String? location;
  final bool isOpened;
  final DateTime? openedAt;
  final String? cost;
  final int createdBy;
  final DateTime createdAt;
  final DateTime updatedAt;

  FridgeItem({
    required this.id,
    required this.foodId,
    required this.foodName,
    required this.groupId,
    required this.quantity,
    this.unitId,
    this.unitName,
    this.note,
    this.purchaseDate,
    required this.useWithinDate,
    this.location,
    required this.isOpened,
    this.openedAt,
    this.cost,
    required this.createdBy,
    required this.createdAt,
    required this.updatedAt,
  });

  factory FridgeItem.fromJson(Map<String, dynamic> json) {
    return FridgeItem(
      id: json['id'],
      foodId: json['foodId'],
      foodName: json['foodName'],
      groupId: json['groupId'],
      quantity: json['quantity'].toString(),
      unitId: json['unitId'],
      unitName: json['unitName'],
      note: json['note'],
      purchaseDate: json['purchaseDate'] != null ? DateTime.parse(json['purchaseDate']) : null,
      useWithinDate: DateTime.parse(json['useWithinDate']),
      location: json['location'],
      isOpened: json['isOpened'],
      openedAt: json['openedAt'] != null ? DateTime.parse(json['openedAt']) : null,
      cost: json['cost']?.toString(),
      createdBy: json['createdBy'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }

  int get daysUntilExpiry => useWithinDate.difference(DateTime.now()).inDays;
  
  bool get isExpired => daysUntilExpiry < 0;
  bool get isExpiringSoon => daysUntilExpiry >= 0 && daysUntilExpiry <= 3;
}
