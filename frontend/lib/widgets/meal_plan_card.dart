import 'package:flutter/material.dart';
import '../models/meal_plan.dart';

class MealPlanCard extends StatelessWidget {
  final MealPlan plan;
  final VoidCallback onTap;

  const MealPlanCard({
    super.key,
    required this.plan,
    required this.onTap,
  });

  Color _getMealTypeColor() {
    switch (plan.mealType.toLowerCase()) {
      case 'breakfast':
        return Colors.orange;
      case 'lunch':
        return Colors.blue;
      case 'dinner':
        return Colors.purple;
      case 'snack':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  IconData _getMealTypeIcon() {
    switch (plan.mealType.toLowerCase()) {
      case 'breakfast':
        return Icons.free_breakfast;
      case 'lunch':
        return Icons.lunch_dining;
      case 'dinner':
        return Icons.dinner_dining;
      case 'snack':
        return Icons.fastfood;
      default:
        return Icons.restaurant;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              // Meal type icon
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: _getMealTypeColor().withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  _getMealTypeIcon(),
                  color: _getMealTypeColor(),
                  size: 28,
                ),
              ),
              const SizedBox(width: 12),
              // Meal details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      plan.foodName,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      plan.mealType.toUpperCase(),
                      style: TextStyle(
                        fontSize: 12,
                        color: _getMealTypeColor(),
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    if (plan.servingSize != null) ...[
                      const SizedBox(height: 2),
                      Text(
                        '${plan.servingSize} ${plan.unitName ?? 'servings'}',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey.shade600,
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              // Prepared indicator
              if (plan.isPrepared)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.green.shade100,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        Icons.check_circle,
                        size: 14,
                        color: Colors.green,
                      ),
                      SizedBox(width: 4),
                      Text(
                        'Prepared',
                        style: TextStyle(
                          fontSize: 10,
                          color: Colors.green,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
