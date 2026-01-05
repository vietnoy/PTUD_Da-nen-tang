import 'package:dio/dio.dart';
import 'api_client.dart';

class AnalyticsService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> getMonthlySpending() async {
    try {
      final response = await _apiClient.dio.get('/analytics/spending/monthly');
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getCategoryBreakdown({String? month}) async {
    try {
      final response = await _apiClient.dio.get(
        '/analytics/categories/breakdown',
        queryParameters: month != null ? {'month': month} : null,
      );
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getSummary() async {
    try {
      final response = await _apiClient.dio.get('/analytics/summary');
      return response.data;
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
