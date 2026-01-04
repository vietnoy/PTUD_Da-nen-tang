class Food {
  final int id;
  final String name;
  final String? description;
  final int categoryId;
  final String? categoryName;
  final int unitId;
  final String? unitName;
  final int groupId;
  final String? imageUrl;
  final bool isActive;
  final int createdBy;
  final DateTime createdAt;
  final DateTime updatedAt;

  Food({
    required this.id,
    required this.name,
    this.description,
    required this.categoryId,
    this.categoryName,
    required this.unitId,
    this.unitName,
    required this.groupId,
    this.imageUrl,
    required this.isActive,
    required this.createdBy,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Food.fromJson(Map<String, dynamic> json) {
    return Food(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      categoryId: json['categoryId'],
      categoryName: json['categoryName'],
      unitId: json['unitId'],
      unitName: json['unitName'],
      groupId: json['groupId'],
      imageUrl: json['imageUrl'],
      isActive: json['isActive'],
      createdBy: json['createdBy'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}
