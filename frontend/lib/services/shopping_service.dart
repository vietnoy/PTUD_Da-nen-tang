import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/shopping_list.dart';
import '../models/shopping_task.dart';

class ShoppingService {
  final ApiClient _apiClient = ApiClient();

  // Shopping Lists
  Future<Map<String, dynamic>> createShoppingList({
    required String name,
    String? description,
    int? assignToId,
    DateTime? dueDate,
    String status = 'pending',
    String priority = 'medium',
    String? budget,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/shopping/list',
        data: {
          'name': name,
          if (description != null) 'description': description,
          if (assignToId != null) 'assignToId': assignToId,
          if (dueDate != null) 'dueDate': dueDate.toIso8601String(),
          'status': status,
          'priority': priority,
          if (budget != null) 'budget': budget,
        },
      );

      return {
        'shoppingList': ShoppingList.fromJson(response.data['shoppingList']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<ShoppingList>> getAllShoppingLists() async {
    try {
      final response = await _apiClient.dio.get('/shopping/list');

      final lists = (response.data['shoppingLists'] as List)
          .map((json) => ShoppingList.fromJson(json))
          .toList();

      return lists;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getShoppingListById(int id) async {
    try {
      final response = await _apiClient.dio.post(
        '/shopping/list/id',
        data: {'listId': id},
      );

      final tasks = (response.data['tasks'] as List)
          .map((json) => ShoppingTask.fromJson(json))
          .toList();

      return {
        'shoppingList': ShoppingList.fromJson(response.data['shoppingList']),
        'tasks': tasks,
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateShoppingList({
    required int listId,
    String? name,
    String? description,
    int? assignToId,
    DateTime? dueDate,
    String? status,
    String? priority,
    String? budget,
  }) async {
    try {
      final Map<String, dynamic> data = {'listId': listId};

      if (name != null) data['name'] = name;
      if (description != null) data['description'] = description;
      if (assignToId != null) data['assignToId'] = assignToId;
      if (dueDate != null) data['dueDate'] = dueDate.toIso8601String();
      if (status != null) data['status'] = status;
      if (priority != null) data['priority'] = priority;
      if (budget != null) data['budget'] = budget;

      final response = await _apiClient.dio.put('/shopping/list', data: data);

      return {
        'shoppingList': ShoppingList.fromJson(response.data['shoppingList']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> deleteShoppingList(int listId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/shopping/list',
        data: {'id': listId},
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  // Shopping Tasks
  Future<Map<String, dynamic>> addShoppingTasks({
    required int listId,
    required List<Map<String, dynamic>> tasks,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/shopping/task',
        data: {'listId': listId, 'tasks': tasks},
      );

      final createdTasks = (response.data['tasks'] as List)
          .map((json) => ShoppingTask.fromJson(json))
          .toList();

      return {
        'tasks': createdTasks,
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> updateShoppingTask({
    required int taskId,
    int? foodId,
    String? quantity,
    int? unitId,
    String? note,
    bool? isDone,
    String? estimatedCost,
    String? actualCost,
    String? priority,
  }) async {
    try {
      final Map<String, dynamic> data = {'taskId': taskId};

      if (foodId != null) data['foodId'] = foodId;
      if (quantity != null) data['newQuantity'] = quantity;
      if (unitId != null) data['unitId'] = unitId;
      if (note != null) data['newNote'] = note;
      if (isDone != null) data['isDone'] = isDone;
      if (estimatedCost != null) data['newEstimatedCost'] = estimatedCost;
      if (actualCost != null) data['actualCost'] = actualCost;
      if (priority != null) data['priority'] = priority;

      final response = await _apiClient.dio.put('/shopping/task', data: data);

      return {
        'task': ShoppingTask.fromJson(response.data['task']),
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> deleteShoppingTask(int taskId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/shopping/task',
        data: {'taskId': taskId},
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
