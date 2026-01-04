class Group {
  final int id;
  final String name;
  final int ownerId;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;

  Group({
    required this.id,
    required this.name,
    required this.ownerId,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Group.fromJson(Map<String, dynamic> json) {
    return Group(
      id: json['id'],
      name: json['name'],
      ownerId: json['ownerId'],
      isActive: json['isActive'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}

class GroupMember {
  final int id;
  final int? userId;
  final int? groupId;
  final String role;
  final String username;
  final String name;
  final String? avatar;
  final DateTime joinedAt;

  GroupMember({
    required this.id,
    this.userId,
    this.groupId,
    required this.role,
    required this.username,
    required this.name,
    this.avatar,
    required this.joinedAt,
  });

  factory GroupMember.fromJson(Map<String, dynamic> json) {
    return GroupMember(
      id: json['id'],
      userId: json['userId'],
      groupId: json['groupId'],
      role: json['role'],
      username: json['username'] ?? '',
      name: json['name'],
      avatar: json['avatarUrl'],
      joinedAt: DateTime.parse(json['joinedAt']),
    );
  }
}
