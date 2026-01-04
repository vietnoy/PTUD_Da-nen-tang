import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/api_client.dart';

class AuthProvider with ChangeNotifier {
  final AuthService _authService = AuthService();
  final ApiClient _apiClient = ApiClient();

  User? _user;
  int? _groupId;
  String? _confirmToken;
  bool _isAuthenticated = false;
  bool _isLoading = true;
  String? _errorMessage;

  User? get user => _user;
  int? get groupId => _groupId;
  String? get confirmToken => _confirmToken;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  AuthProvider() {
    _checkAuthStatus();
  }

  Future<void> _checkAuthStatus() async {
    try {
      final accessToken = await _apiClient.getAccessToken();
      final refreshToken = await _apiClient.getRefreshToken();

      if (accessToken != null && refreshToken != null) {
        final prefs = await SharedPreferences.getInstance();
        final userId = prefs.getInt('userId');
        final userEmail = prefs.getString('userEmail');
        final userName = prefs.getString('userName');
        final username = prefs.getString('username');
        final userLanguage = prefs.getString('userLanguage');
        final userTimezone = prefs.getInt('userTimezone');
        final isVerified = prefs.getBool('isVerified');
        final avatar = prefs.getString('avatar');
        _groupId = prefs.getInt('groupId');

        if (userId != null && userEmail != null && userName != null && username != null) {
          _user = User(
            id: userId,
            email: userEmail,
            name: userName,
            username: username,
            language: userLanguage ?? 'en',
            timezone: userTimezone ?? 7,
            isActive: true,
            isVerified: isVerified ?? false,
            avatar: avatar,
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          );
          _isAuthenticated = true;
        }
      }
    } catch (e) {
      _isAuthenticated = false;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> login(String email, String password) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _authService.login(email, password);

      await _apiClient.saveTokens(
        result['accessToken'],
        result['refreshToken'],
      );

      _user = result['user'];
      _groupId = result['groupId'];
      _isAuthenticated = true;

      await _saveUserData(_user!, _groupId!);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> setActiveGroup(int groupId) async {
    _groupId = groupId;
    if (_user != null) {
      await _saveUserData(_user!, groupId);
    }
    notifyListeners();
  }

  Future<bool> register({
    required String email,
    required String password,
    required String name,
    required String username,
    String language = 'en',
    int timezone = 7,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _authService.register(
        email: email,
        password: password,
        name: name,
        username: username,
        language: language,
        timezone: timezone,
      );

      _user = result['user'];
      _groupId = result['groupId'];
      _confirmToken = result['confirmToken'];

      // Even if saving fails, registration succeeded if we have confirmToken
      try {
        await _saveUserData(_user!, _groupId!);
      } catch (saveError) {
        // Ignore save errors - we can still proceed with verification
        print('Failed to save user data: $saveError');
      }

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      // Only show error if registration actually failed
      if (e.toString().contains('confirmToken') ||
          e.toString().contains('user') ||
          e.toString().contains('resultCode')) {
        _errorMessage = e.toString();
      }
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> verifyEmail(String code) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      if (_confirmToken == null) {
        throw Exception('No confirmation token available');
      }

      final result = await _authService.verifyEmail(_confirmToken!, code);

      await _apiClient.saveTokens(
        result['accessToken'],
        result['refreshToken'],
      );

      _user = result['user'];
      _groupId = result['groupId'];
      _isAuthenticated = true;

      await _saveUserData(_user!, _groupId!);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    try {
      await _authService.logout();
    } finally {
      await _clearUserData();
      _user = null;
      _groupId = null;
      _isAuthenticated = false;
      notifyListeners();
    }
  }

  Future<bool> updateProfile({
    String? name,
    String? username,
    String? language,
    int? timezone,
    dynamic avatar,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _authService.editProfile(
        name: name,
        username: username,
        language: language,
        timezone: timezone,
        avatar: avatar,
      );

      _user = result['user'];
      await _saveUserData(_user!, _groupId!);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> _saveUserData(User user, int groupId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('userId', user.id);
    await prefs.setString('userEmail', user.email);
    await prefs.setString('userName', user.name);
    await prefs.setString('username', user.username);
    await prefs.setString('userLanguage', user.language);
    await prefs.setInt('userTimezone', user.timezone);
    await prefs.setBool('isVerified', user.isVerified);
    if (user.avatar != null) {
      await prefs.setString('avatar', user.avatar!);
    }
    await prefs.setInt('groupId', groupId);
  }

  Future<void> _clearUserData() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }
}
