import 'package:flutter/foundation.dart';
import '../models/food.dart';
import '../services/food_service.dart';

class FoodProvider with ChangeNotifier {
  final FoodService _foodService = FoodService();

  List<Food> _foods = [];
  List<Map<String, dynamic>> _units = [];
  List<Map<String, dynamic>> _categories = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<Food> get foods => _foods;
  List<Map<String, dynamic>> get units => _units;
  List<Map<String, dynamic>> get categories => _categories;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  Future<void> loadFoods() async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _foods = await _foodService.getAllFoods();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadUnits() async {
    try {
      _units = await _foodService.getAllUnits();
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }

  Future<void> loadCategories() async {
    try {
      _categories = await _foodService.getAllCategories();
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }

  Future<bool> createFood({
    required String name,
    required int groupId,
    String? description,
    int? categoryId,
    int? defaultUnitId,
    String? brand,
    int? defaultShelfLifeDays,
    String? storageInstructions,
    dynamic image,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      // Convert category ID to name
      String? categoryName;
      if (categoryId != null) {
        final category = _categories.firstWhere(
          (cat) => cat['id'] == categoryId,
          orElse: () => {},
        );
        categoryName = category['name'];
      }

      // Convert unit ID to name
      String? unitName;
      if (defaultUnitId != null) {
        final unit = _units.firstWhere(
          (u) => u['id'] == defaultUnitId,
          orElse: () => {},
        );
        unitName = unit['name'];
      }

      if (categoryName == null || unitName == null) {
        throw Exception('Category or unit not found');
      }

      final result = await _foodService.createFood(
        name: name,
        categoryName: categoryName,
        unitName: unitName,
        groupId: groupId,
        description: description,
        brand: brand,
        defaultShelfLifeDays: defaultShelfLifeDays,
        storageInstructions: storageInstructions,
        image: image,
      );

      _foods.add(result['food']);

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

  Future<bool> updateFood({
    required int foodId,
    String? name,
    String? description,
    int? categoryId,
    int? defaultUnitId,
    dynamic image,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _foodService.updateFood(
        foodId: foodId,
        name: name,
        description: description,
        categoryId: categoryId,
        defaultUnitId: defaultUnitId,
        image: image,
      );

      final index = _foods.indexWhere((food) => food.id == foodId);
      if (index != -1) {
        _foods[index] = result['food'];
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

  Future<bool> deleteFood(int foodId) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      await _foodService.deleteFood(foodId);

      _foods.removeWhere((food) => food.id == foodId);

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

  Food? getFoodById(int id) {
    try {
      return _foods.firstWhere((food) => food.id == id);
    } catch (e) {
      return null;
    }
  }

  List<Food> searchFoods(String query) {
    if (query.isEmpty) return _foods;
    
    final lowerQuery = query.toLowerCase();
    return _foods.where((food) {
      return food.name.toLowerCase().contains(lowerQuery) ||
          (food.description?.toLowerCase().contains(lowerQuery) ?? false);
    }).toList();
  }
}
