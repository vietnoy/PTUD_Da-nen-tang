import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/user.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/login',
        data: {'email': email, 'password': password},
      );

      final user = User.fromJson(response.data['user']);
      final groupId = response.data['groupId'] ??
                     response.data['user']['belongsToGroupAdminId'] ??
                     0;

      return {
        'accessToken': response.data['accessToken'],
        'refreshToken': response.data['refreshToken'],
        'user': user,
        'groupId': groupId,
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String name,
    required String username,
    String language = 'en',
    int timezone = 7,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/register',
        data: {
          'email': email,
          'password': password,
          'name': name,
          'user_name': username,
          'language': language,
          'timezone': timezone,
          'deviceId': 'web-browser-${DateTime.now().millisecondsSinceEpoch}',
        },
      );

      return {
        'user': User.fromJson(response.data['user']),
        'groupId': response.data['groupId'],
        'confirmToken': response.data['confirmToken'],
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> sendVerificationCode(String email) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/send-verification-code',
        data: {'email': email},
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> verifyEmail(String confirmToken, String code) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/verify-email',
        data: {'confirmToken': confirmToken, 'code': code},
      );

      final user = User.fromJson(response.data['user']);
      final groupId = response.data['groupId'] ??
                     response.data['user']['belongsToGroupAdminId'] ??
                     0;

      return {
        'accessToken': response.data['accessToken'],
        'refreshToken': response.data['refreshToken'],
        'user': user,
        'groupId': groupId,
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> logout() async {
    try {
      await _apiClient.dio.post('/auth/logout');
      await _apiClient.clearTokens();
    } on DioException catch (e) {
      await _apiClient.clearTokens();
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> editProfile({
    String? name,
    String? username,
    String? language,
    int? timezone,
    MultipartFile? avatar,
  }) async {
    try {
      final formData = FormData();
      if (name != null) formData.fields.add(MapEntry('name', name));
      if (username != null) formData.fields.add(MapEntry('username', username));
      if (language != null) formData.fields.add(MapEntry('language', language));
      if (timezone != null) formData.fields.add(MapEntry('timezone', timezone.toString()));
      if (avatar != null) formData.files.add(MapEntry('file', avatar));

      final response = await _apiClient.dio.put(
        '/users/me',
        data: formData,
      );

      return {
        'user': User.fromJson(response.data['user']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/auth/user/change-password',
        data: {
          'currentPassword': currentPassword,
          'newPassword': newPassword,
        },
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException e) {
    if (e.response != null) {
      final resultMessage = e.response?.data['resultMessage'];
      if (resultMessage != null) {
        return resultMessage['en'] ?? 'An error occurred';
      }
    }
    return e.message ?? 'Network error';
  }
}
