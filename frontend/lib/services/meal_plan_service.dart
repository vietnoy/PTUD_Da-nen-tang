import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/meal_plan.dart';

class MealPlanService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> createMealPlan({
    required int foodId,
    required String mealType,
    required DateTime mealDate,
    String? servingSize,
    int? unitId,
    String? note,
    bool isPrepared = false,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/meal-plans/',
        data: {
          'foodId': foodId,
          'mealType': mealType,
          'mealDate': mealDate.toIso8601String(),
          if (servingSize != null) 'servingSize': servingSize,
          if (unitId != null) 'unitId': unitId,
          if (note != null) 'note': note,
          'isPrepared': isPrepared,
        },
      );

      return {
        'mealPlan': MealPlan.fromJson(response.data['mealPlan']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<MealPlan>> getAllMealPlans({
    DateTime? startDate,
    DateTime? endDate,
    String? mealType,
  }) async {
    try {
      final queryParams = <String, dynamic>{};
      if (startDate != null) queryParams['startDate'] = startDate.toIso8601String();
      if (endDate != null) queryParams['endDate'] = endDate.toIso8601String();
      if (mealType != null) queryParams['mealType'] = mealType;

      final response = await _apiClient.dio.get(
        '/meal-plans/',
        queryParameters: queryParams,
      );

      final mealPlans = (response.data['mealPlans'] as List)
          .map((json) => MealPlan.fromJson(json))
          .toList();

      return mealPlans;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<MealPlan> getMealPlanById(int id) async {
    try {
      final response = await _apiClient.dio.post(
        '/meal-plans/id/',
        data: {'mealPlanId': id},
      );

      return MealPlan.fromJson(response.data['mealPlan']);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateMealPlan({
    required int mealPlanId,
    int? foodId,
    String? mealType,
    DateTime? mealDate,
    String? servingSize,
    int? unitId,
    String? note,
    bool? isPrepared,
  }) async {
    try {
      final Map<String, dynamic> data = {'mealPlanId': mealPlanId};

      if (foodId != null) data['foodId'] = foodId;
      if (mealType != null) data['mealType'] = mealType;
      if (mealDate != null) data['mealDate'] = mealDate.toIso8601String();
      if (servingSize != null) data['servingSize'] = servingSize;
      if (unitId != null) data['unitId'] = unitId;
      if (note != null) data['note'] = note;
      if (isPrepared != null) data['isPrepared'] = isPrepared;

      final response = await _apiClient.dio.put('/meal-plans/', data: data);

      return {
        'mealPlan': MealPlan.fromJson(response.data['mealPlan']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> deleteMealPlan(int mealPlanId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/meal-plans/',
        data: {'mealPlanId': mealPlanId},
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
