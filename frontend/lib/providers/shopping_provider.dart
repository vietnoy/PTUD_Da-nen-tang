import 'package:flutter/foundation.dart';
import '../models/shopping_list.dart';
import '../models/shopping_task.dart';
import '../services/shopping_service.dart';

class ShoppingProvider with ChangeNotifier {
  final ShoppingService _shoppingService = ShoppingService();

  List<ShoppingList> _shoppingLists = [];
  Map<int, List<ShoppingTask>> _tasksByListId = {};
  bool _isLoading = false;
  String? _errorMessage;

  List<ShoppingList> get shoppingLists => _shoppingLists;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  List<ShoppingTask> getTasksForList(int listId) {
    return _tasksByListId[listId] ?? [];
  }

  Future<void> loadShoppingLists() async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _shoppingLists = await _shoppingService.getAllShoppingLists();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadShoppingListDetails(int listId) async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      final result = await _shoppingService.getShoppingListById(listId);
      
      _tasksByListId[listId] = result['tasks'];

      final index = _shoppingLists.indexWhere((list) => list.id == listId);
      if (index != -1) {
        _shoppingLists[index] = result['shoppingList'];
      }

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createShoppingList({
    required String name,
    String? description,
    int? assignToId,
    DateTime? dueDate,
    String status = 'pending',
    String priority = 'medium',
    String? budget,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _shoppingService.createShoppingList(
        name: name,
        description: description,
        assignToId: assignToId,
        dueDate: dueDate,
        status: status,
        priority: priority,
        budget: budget,
      );

      _shoppingLists.add(result['shoppingList']);

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

  Future<bool> updateShoppingList({
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
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _shoppingService.updateShoppingList(
        listId: listId,
        name: name,
        description: description,
        assignToId: assignToId,
        dueDate: dueDate,
        status: status,
        priority: priority,
        budget: budget,
      );

      final index = _shoppingLists.indexWhere((list) => list.id == listId);
      if (index != -1) {
        _shoppingLists[index] = result['shoppingList'];
      }

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

  Future<bool> deleteShoppingList(int listId) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      await _shoppingService.deleteShoppingList(listId);

      _shoppingLists.removeWhere((list) => list.id == listId);
      _tasksByListId.remove(listId);

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

  Future<bool> addShoppingTasks({
    required int listId,
    required List<Map<String, dynamic>> tasks,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _shoppingService.addShoppingTasks(
        listId: listId,
        tasks: tasks,
      );

      if (_tasksByListId.containsKey(listId)) {
        _tasksByListId[listId]!.addAll(result['tasks']);
      } else {
        _tasksByListId[listId] = result['tasks'];
      }

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

  Future<bool> updateShoppingTask({
    required int taskId,
    required int listId,
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
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _shoppingService.updateShoppingTask(
        taskId: taskId,
        foodId: foodId,
        quantity: quantity,
        unitId: unitId,
        note: note,
        isDone: isDone,
        estimatedCost: estimatedCost,
        actualCost: actualCost,
        priority: priority,
      );

      if (_tasksByListId.containsKey(listId)) {
        final index = _tasksByListId[listId]!.indexWhere((task) => task.id == taskId);
        if (index != -1) {
          _tasksByListId[listId]![index] = result['task'];
        }
      }

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

  Future<bool> deleteShoppingTask(int taskId, int listId) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      await _shoppingService.deleteShoppingTask(taskId);

      if (_tasksByListId.containsKey(listId)) {
        _tasksByListId[listId]!.removeWhere((task) => task.id == taskId);
      }

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
}
