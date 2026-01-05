class MealPlan {
  final int id;
  final int foodId;
  final String foodName;
  final int groupId;
  final String mealType;
  final DateTime mealDate;
  final String? servingSize;
  final int? unitId;
  final String? unitName;
  final String? note;
  final bool isPrepared;
  final int createdBy;
  final String? createdByUsername;
  final DateTime createdAt;
  final DateTime updatedAt;

  MealPlan({
    required this.id,
    required this.foodId,
    required this.foodName,
    required this.groupId,
    required this.mealType,
    required this.mealDate,
    this.servingSize,
    this.unitId,
    this.unitName,
    this.note,
    required this.isPrepared,
    required this.createdBy,
    this.createdByUsername,
    required this.createdAt,
    required this.updatedAt,
  });

  factory MealPlan.fromJson(Map<String, dynamic> json) {
    return MealPlan(
      id: json['id'],
      foodId: json['foodId'],
      foodName: json['foodName'],
      groupId: json['groupId'],
      mealType: json['mealType'],
      mealDate: DateTime.parse(json['mealDate']),
      servingSize: json['servingSize']?.toString(),
      unitId: json['unitId'],
      unitName: json['unitName'],
      note: json['note'],
      isPrepared: json['isPrepared'],
      createdBy: json['createdBy'],
      createdByUsername: json['createdByUsername'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}
