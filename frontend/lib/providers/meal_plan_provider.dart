import 'package:flutter/foundation.dart';
import '../models/meal_plan.dart';
import '../services/meal_plan_service.dart';

class MealPlanProvider with ChangeNotifier {
  final MealPlanService _mealPlanService = MealPlanService();

  List<MealPlan> _mealPlans = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<MealPlan> get mealPlans => _mealPlans;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  List<MealPlan> getMealPlansForDate(DateTime date) {
    return _mealPlans.where((plan) {
      return plan.mealDate.year == date.year &&
          plan.mealDate.month == date.month &&
          plan.mealDate.day == date.day;
    }).toList();
  }

  List<MealPlan> getMealPlansForDateRange(DateTime startDate, DateTime endDate) {
    return _mealPlans.where((plan) {
      return plan.mealDate.isAfter(startDate.subtract(const Duration(days: 1))) &&
          plan.mealDate.isBefore(endDate.add(const Duration(days: 1)));
    }).toList();
  }

  List<MealPlan> getMealPlansByType(String mealType) {
    return _mealPlans.where((plan) => plan.mealType == mealType).toList();
  }

  Future<void> loadMealPlans({
    DateTime? startDate,
    DateTime? endDate,
    String? mealType,
  }) async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _mealPlans = await _mealPlanService.getAllMealPlans(
        startDate: startDate,
        endDate: endDate,
        mealType: mealType,
      );

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> createMealPlan({
    required int foodId,
    required String mealType,
    required DateTime mealDate,
    String? servingSize,
    int? unitId,
    String? note,
    bool isPrepared = false,
  }) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _mealPlanService.createMealPlan(
        foodId: foodId,
        mealType: mealType,
        mealDate: mealDate,
        servingSize: servingSize,
        unitId: unitId,
        note: note,
        isPrepared: isPrepared,
      );

      _mealPlans.add(result['mealPlan']);

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

  Future<bool> updateMealPlan({
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
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      final result = await _mealPlanService.updateMealPlan(
        mealPlanId: mealPlanId,
        foodId: foodId,
        mealType: mealType,
        mealDate: mealDate,
        servingSize: servingSize,
        unitId: unitId,
        note: note,
        isPrepared: isPrepared,
      );

      final index = _mealPlans.indexWhere((plan) => plan.id == mealPlanId);
      if (index != -1) {
        _mealPlans[index] = result['mealPlan'];
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

  Future<bool> deleteMealPlan(int mealPlanId) async {
    try {
      _errorMessage = null;
      _isLoading = true;
      notifyListeners();

      await _mealPlanService.deleteMealPlan(mealPlanId);

      _mealPlans.removeWhere((plan) => plan.id == mealPlanId);

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

  Future<bool> togglePreparedStatus(int mealPlanId) async {
    final mealPlan = _mealPlans.firstWhere((plan) => plan.id == mealPlanId);
    return await updateMealPlan(
      mealPlanId: mealPlanId,
      isPrepared: !mealPlan.isPrepared,
    );
  }
}
