class User {
  final int id;
  final String email;
  final String name;
  final String username;
  final String language;
  final int timezone;
  final bool isActive;
  final bool isVerified;
  final String? avatar;
  final DateTime createdAt;
  final DateTime updatedAt;

  User({
    required this.id,
    required this.email,
    required this.name,
    required this.username,
    required this.language,
    required this.timezone,
    required this.isActive,
    required this.isVerified,
    this.avatar,
    required this.createdAt,
    required this.updatedAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      username: json['username'],
      language: json['language'],
      timezone: json['timezone'],
      isActive: json['isActivated'] ?? json['isActive'] ?? true,
      isVerified: json['isVerified'] ?? false,
      avatar: json['photoUrl'] ?? json['avatar'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'username': username,
      'language': language,
      'timezone': timezone,
      'isActive': isActive,
      'isVerified': isVerified,
      'avatar': avatar,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }
}
