import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/fridge_item.dart';

class FridgeService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> createFridgeItem({
    required int foodId,
    required String quantity,
    int? unitId,
    String? note,
    DateTime? purchaseDate,
    required DateTime useWithinDate,
    String? location,
    bool isOpened = false,
    DateTime? openedAt,
    String? cost,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/fridge/',
        data: {
          'foodId': foodId,
          'quantity': quantity,
          if (unitId != null) 'unitId': unitId,
          if (note != null) 'note': note,
          if (purchaseDate != null) 'purchaseDate': purchaseDate.toIso8601String(),
          'useWithinDate': useWithinDate.toIso8601String(),
          if (location != null) 'location': location,
          'isOpened': isOpened,
          if (openedAt != null) 'openedAt': openedAt.toIso8601String(),
          if (cost != null) 'cost': cost,
        },
      );

      return {
        'fridgeItem': FridgeItem.fromJson(response.data['fridgeItem']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<FridgeItem>> getAllFridgeItems() async {
    try {
      final response = await _apiClient.dio.get('/fridge/');

      final items = (response.data['fridgeItems'] as List)
          .map((json) => FridgeItem.fromJson(json))
          .toList();

      return items;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<FridgeItem> getFridgeItemById(int id) async {
    try {
      final response = await _apiClient.dio.post(
        '/fridge/id/',
        data: {'fridgeItemId': id},
      );

      return FridgeItem.fromJson(response.data['fridgeItem']);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateFridgeItem({
    required int fridgeItemId,
    int? foodId,
    String? quantity,
    int? unitId,
    String? note,
    DateTime? purchaseDate,
    DateTime? useWithinDate,
    String? location,
    bool? isOpened,
    DateTime? openedAt,
    String? cost,
  }) async {
    try {
      final Map<String, dynamic> data = {'id': fridgeItemId};

      if (foodId != null) data['foodId'] = foodId;
      if (quantity != null) data['quantity'] = quantity;
      if (unitId != null) data['unitId'] = unitId;
      if (note != null) data['note'] = note;
      if (purchaseDate != null) data['purchaseDate'] = purchaseDate.toIso8601String();
      if (useWithinDate != null) data['useWithinDate'] = useWithinDate.toIso8601String();
      if (location != null) data['location'] = location;
      if (isOpened != null) data['isOpened'] = isOpened;
      if (openedAt != null) data['openedAt'] = openedAt.toIso8601String();
      if (cost != null) data['cost'] = cost;

      final response = await _apiClient.dio.put('/fridge/', data: data);

      return {
        'fridgeItem': FridgeItem.fromJson(response.data['fridgeItem']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> deleteFridgeItem(int fridgeItemId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/fridge/',
        data: {'id': fridgeItemId},
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
