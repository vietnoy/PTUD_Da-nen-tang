import 'package:dio/dio.dart';
import 'api_client.dart';

class AdminService {
  final ApiClient _apiClient = ApiClient();

  // ==================== ADMIN LOGIN ====================

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      print('AdminService: Attempting login to ${_apiClient.dio.options.baseUrl}/admin/login');
      print('AdminService: Username: $username');
      
      final response = await _apiClient.dio.post(
        '/admin/login',
        data: {'username': username, 'password': password},
      );

      print('AdminService: Login response: ${response.data}');

      // Save admin token
      _apiClient.dio.options.headers['Authorization'] = 'Bearer ${response.data['accessToken']}';

      return {
        'accessToken': response.data['accessToken'],
        'username': response.data['username'],
        'resultCode': response.data['resultCode'],
      };
    } on DioException catch (e) {
      print('AdminService: DioException - ${e.type}');
      print('AdminService: Error message - ${e.message}');
      print('AdminService: Response - ${e.response?.data}');
      throw _handleError(e);
    } catch (e) {
      print('AdminService: General exception - $e');
      rethrow;
    }
  }

  // ==================== USER MANAGEMENT ====================

  Future<Map<String, dynamic>> getAllUsers({int skip = 0, int limit = 100}) async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/users',
        queryParameters: {'skip': skip, 'limit': limit},
      );

      return {
        'users': (response.data['users'] as List).map((user) => user).toList(),
        'total': response.data['total'],
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getUserById(int userId) async {
    try {
      final response = await _apiClient.dio.get('/admin/users/$userId');
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> createUser(Map<String, dynamic> userData) async {
    try {
      final response = await _apiClient.dio.post(
        '/admin/users',
        data: userData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateUser(int userId, Map<String, dynamic> userData) async {
    try {
      final response = await _apiClient.dio.put(
        '/admin/users/$userId',
        data: userData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteUser(int userId) async {
    try {
      await _apiClient.dio.delete('/admin/users/$userId');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // ==================== UNIT MANAGEMENT ====================

  Future<Map<String, dynamic>> getAllUnits({int skip = 0, int limit = 100}) async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/units',
        queryParameters: {'skip': skip, 'limit': limit},
      );

      return {
        'units': (response.data['units'] as List).map((unit) => unit).toList(),
        'total': response.data['total'],
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getUnitById(int unitId) async {
    try {
      final response = await _apiClient.dio.get('/admin/units/$unitId');
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> createUnit(Map<String, dynamic> unitData) async {
    try {
      final response = await _apiClient.dio.post(
        '/admin/units',
        data: unitData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateUnit(int unitId, Map<String, dynamic> unitData) async {
    try {
      final response = await _apiClient.dio.put(
        '/admin/units/$unitId',
        data: unitData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteUnit(int unitId) async {
    try {
      await _apiClient.dio.delete('/admin/units/$unitId');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // ==================== CATEGORY MANAGEMENT ====================

  Future<Map<String, dynamic>> getAllCategories({int skip = 0, int limit = 100}) async {
    try {
      final response = await _apiClient.dio.get(
        '/admin/categories',
        queryParameters: {'skip': skip, 'limit': limit},
      );

      return {
        'categories': (response.data['categories'] as List).map((category) => category).toList(),
        'total': response.data['total'],
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getCategoryById(int categoryId) async {
    try {
      final response = await _apiClient.dio.get('/admin/categories/$categoryId');
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> createCategory(Map<String, dynamic> categoryData) async {
    try {
      final response = await _apiClient.dio.post(
        '/admin/categories',
        data: categoryData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateCategory(int categoryId, Map<String, dynamic> categoryData) async {
    try {
      final response = await _apiClient.dio.put(
        '/admin/categories/$categoryId',
        data: categoryData,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteCategory(int categoryId) async {
    try {
      await _apiClient.dio.delete('/admin/categories/$categoryId');
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // ==================== ERROR HANDLING ====================

  String _handleError(DioException error) {
    if (error.response != null) {
      final detail = error.response?.data['detail'];
      if (detail != null) {
        return detail.toString();
      }
      return 'Server error: ${error.response?.statusCode}';
    } else if (error.type == DioExceptionType.connectionTimeout) {
      return 'Connection timeout';
    } else if (error.type == DioExceptionType.receiveTimeout) {
      return 'Receive timeout';
    } else {
      return 'Network error: ${error.message}';
    }
  }
}
