import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/food.dart';

class FoodService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> createFood({
    required String name,
    required String categoryName,
    required String unitName,
    required int groupId,
    String? description,
    String? brand,
    int? defaultShelfLifeDays,
    String? storageInstructions,
    MultipartFile? image,
  }) async {
    try {
      final formData = FormData();
      formData.fields.add(MapEntry('name', name));
      formData.fields.add(MapEntry('category_name', categoryName));
      formData.fields.add(MapEntry('unit_name', unitName));
      formData.fields.add(MapEntry('group_id', groupId.toString()));
      if (description != null && description.isNotEmpty) {
        formData.fields.add(MapEntry('description', description));
      }
      if (brand != null && brand.isNotEmpty) {
        formData.fields.add(MapEntry('brand', brand));
      }
      if (defaultShelfLifeDays != null) {
        formData.fields.add(MapEntry('default_shelf_life_days', defaultShelfLifeDays.toString()));
      }
      if (storageInstructions != null && storageInstructions.isNotEmpty) {
        formData.fields.add(MapEntry('storage_instructions', storageInstructions));
      }
      if (image != null) formData.files.add(MapEntry('image', image));

      // Tạo request với UTF-8 encoding
      final response = await _apiClient.dio.post(
        '/food/',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data; charset=utf-8',
        ),
      );

      return {
        'food': Food.fromJson(response.data['food']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<Food>> getAllFoods() async {
    try {
      final response = await _apiClient.dio.get('/food/');

      final foods = (response.data['foods'] as List)
          .map((json) => Food.fromJson(json))
          .toList();

      return foods;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Food> getFoodById(int id) async {
    try {
      final response = await _apiClient.dio.post(
        '/food/id/',
        data: {'foodId': id},
      );

      return Food.fromJson(response.data['food']);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateFood({
    required int foodId,
    String? name,
    String? description,
    int? categoryId,
    int? defaultUnitId,
    MultipartFile? image,
  }) async {
    try {
      final formData = FormData();
      formData.fields.add(MapEntry('foodId', foodId.toString()));
      if (name != null) formData.fields.add(MapEntry('name', name));
      if (description != null) formData.fields.add(MapEntry('description', description));
      if (categoryId != null) formData.fields.add(MapEntry('categoryId', categoryId.toString()));
      if (defaultUnitId != null) formData.fields.add(MapEntry('defaultUnitId', defaultUnitId.toString()));
      if (image != null) formData.files.add(MapEntry('image', image));

      // Tạo request với UTF-8 encoding
      final response = await _apiClient.dio.put(
        '/food/',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data; charset=utf-8',
        ),
      );

      return {
        'food': Food.fromJson(response.data['food']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> deleteFood(int foodId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/food/',
        data: {'foodId': foodId},
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<Map<String, dynamic>>> getAllUnits() async {
    try {
      final response = await _apiClient.dio.get('/unit/');
      return List<Map<String, dynamic>>.from(response.data['units']);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<Map<String, dynamic>>> getAllCategories() async {
    try {
      final response = await _apiClient.dio.get('/category/');
      return List<Map<String, dynamic>>.from(response.data['categories']);
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
