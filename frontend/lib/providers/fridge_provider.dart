import 'package:flutter/foundation.dart';
import '../models/fridge_item.dart';
import '../services/fridge_service.dart';

class FridgeProvider with ChangeNotifier {
  final FridgeService _fridgeService = FridgeService();

  List<FridgeItem> _fridgeItems = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<FridgeItem> get fridgeItems => _fridgeItems;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  List<FridgeItem> get expiredItems =>
      _fridgeItems.where((item) => item.isExpired).toList();

  List<FridgeItem> get expiringSoonItems =>
      _fridgeItems.where((item) => item.isExpiringSoon).toList();

  List<FridgeItem> getItemsByLocation(String? location) {
    if (location == null) return _fridgeItems;
    return _fridgeItems.where((item) => item.location == location).toList();
  }

  Future<void> loadFridgeItems() async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _fridgeItems = await _fridgeService.getAllFridgeItems();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createFridgeItem({
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
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _fridgeService.createFridgeItem(
        foodId: foodId,
        quantity: quantity,
        unitId: unitId,
        note: note,
        purchaseDate: purchaseDate,
        useWithinDate: useWithinDate,
        location: location,
        isOpened: isOpened,
        openedAt: openedAt,
        cost: cost,
      );

      _fridgeItems.add(result['fridgeItem']);

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

  Future<bool> updateFridgeItem({
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
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _fridgeService.updateFridgeItem(
        fridgeItemId: fridgeItemId,
        foodId: foodId,
        quantity: quantity,
        unitId: unitId,
        note: note,
        purchaseDate: purchaseDate,
        useWithinDate: useWithinDate,
        location: location,
        isOpened: isOpened,
        openedAt: openedAt,
        cost: cost,
      );

      final index = _fridgeItems.indexWhere((item) => item.id == fridgeItemId);
      if (index != -1) {
        _fridgeItems[index] = result['fridgeItem'];
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

  Future<bool> deleteFridgeItem(int fridgeItemId) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      await _fridgeService.deleteFridgeItem(fridgeItemId);

      _fridgeItems.removeWhere((item) => item.id == fridgeItemId);

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
