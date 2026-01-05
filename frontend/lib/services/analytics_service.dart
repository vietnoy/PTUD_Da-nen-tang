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
      final data = e.response?.data;
      if (data is Map && data['resultMessage'] != null) {
        final resultMessage = data['resultMessage'];
        if (resultMessage is Map && resultMessage['en'] != null) {
          return resultMessage['en'].toString();
        } else if (resultMessage is String) {
          return resultMessage;
        }
      }
      if (data is Map && data['detail'] != null) {
        return data['detail'].toString();
      }
    }
    return e.message ?? 'Network error';
  }
}
