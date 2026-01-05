class MonthlySpending {
  final List<String> months;
  final List<double> amounts;
  final List<double> budgets;

  MonthlySpending({
    required this.months,
    required this.amounts,
    required this.budgets,
  });

  factory MonthlySpending.fromJson(Map<String, dynamic> json) {
    return MonthlySpending(
      months: List<String>.from(json['months'] ?? []),
      amounts: (json['amounts'] as List?)?.map((e) => (e as num).toDouble()).toList() ?? [],
      budgets: (json['budgets'] as List?)?.map((e) => (e as num).toDouble()).toList() ?? [],
    );
  }
}

class CategoryData {
  final String name;
  final double amount;
  final double percentage;
  final int itemCount;

  CategoryData({
    required this.name,
    required this.amount,
    required this.percentage,
    required this.itemCount,
  });

  factory CategoryData.fromJson(Map<String, dynamic> json) {
    return CategoryData(
      name: json['name'] ?? '',
      amount: (json['amount'] as num?)?.toDouble() ?? 0.0,
      percentage: (json['percentage'] as num?)?.toDouble() ?? 0.0,
      itemCount: json['itemCount'] ?? 0,
    );
  }
}

class CategoryBreakdown {
  final List<String> categories;
  final List<double> amounts;
  final List<double> percentages;

  CategoryBreakdown({
    required this.categories,
    required this.amounts,
    required this.percentages,
  });

  factory CategoryBreakdown.fromJson(Map<String, dynamic> json) {
    // Extract categories data from the response
    final categoriesList = json['categories'] as List?;
    if (categoriesList != null && categoriesList.isNotEmpty) {
      // Parse from CategoryData objects
      final categoryNames = <String>[];
      final categoryAmounts = <double>[];
      final categoryPercentages = <double>[];
      
      for (var cat in categoriesList) {
        if (cat is Map<String, dynamic>) {
          categoryNames.add(cat['name']?.toString() ?? '');
          categoryAmounts.add((cat['amount'] as num?)?.toDouble() ?? 0.0);
          categoryPercentages.add((cat['percentage'] as num?)?.toDouble() ?? 0.0);
        }
      }
      
      return CategoryBreakdown(
        categories: categoryNames,
        amounts: categoryAmounts,
        percentages: categoryPercentages,
      );
    }
    
    return CategoryBreakdown(
      categories: [],
      amounts: [],
      percentages: [],
    );
  }
}

class AnalyticsSummary {
  final double totalSpent;
  final double totalBudget;
  final double averageShoppingTrip;
  final double fridgeValue;
  final int expiringSoonCount;

  AnalyticsSummary({
    required this.totalSpent,
    required this.totalBudget,
    required this.averageShoppingTrip,
    required this.fridgeValue,
    required this.expiringSoonCount,
  });

  factory AnalyticsSummary.fromJson(Map<String, dynamic> json) {
    return AnalyticsSummary(
      totalSpent: (json['totalSpent'] as num?)?.toDouble() ?? 0.0,
      totalBudget: (json['totalBudget'] as num?)?.toDouble() ?? 0.0,
      averageShoppingTrip: (json['averageShoppingTrip'] as num?)?.toDouble() ?? 0.0,
      fridgeValue: (json['fridgeValue'] as num?)?.toDouble() ?? 0.0,
      expiringSoonCount: json['expiringSoonCount'] ?? 0,
    );
  }
}
