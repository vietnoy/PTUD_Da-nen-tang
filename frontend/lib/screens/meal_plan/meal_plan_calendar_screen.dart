import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:table_calendar/table_calendar.dart';
import '../../providers/meal_plan_provider.dart';
import '../../models/meal_plan.dart';

class MealPlanCalendarScreen extends StatefulWidget {
  const MealPlanCalendarScreen({super.key});

  @override
  State<MealPlanCalendarScreen> createState() => _MealPlanCalendarScreenState();
}

class _MealPlanCalendarScreenState extends State<MealPlanCalendarScreen> {
  DateTime _focusedDay = DateTime.now();
  DateTime? _selectedDay;
  CalendarFormat _calendarFormat = CalendarFormat.month;

  @override
  void initState() {
    super.initState();
    _selectedDay = _focusedDay;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadMealPlans();
    });
  }

  void _loadMealPlans() {
    final startOfMonth = DateTime(_focusedDay.year, _focusedDay.month, 1);
    final endOfMonth = DateTime(_focusedDay.year, _focusedDay.month + 1, 0);
    
    Provider.of<MealPlanProvider>(context, listen: false).loadMealPlans(
      startDate: startOfMonth,
      endDate: endOfMonth,
    );
  }

  List<MealPlan> _getMealPlansForDay(DateTime day) {
    final mealPlanProvider = Provider.of<MealPlanProvider>(context, listen: false);
    return mealPlanProvider.getMealPlansForDate(day);
  }

  @override
  Widget build(BuildContext context) {
    final mealPlanProvider = Provider.of<MealPlanProvider>(context);
    final selectedDayPlans = _selectedDay != null
        ? mealPlanProvider.getMealPlansForDate(_selectedDay!)
        : <MealPlan>[];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Meal Planning'),
      ),
      body: Column(
        children: [
          TableCalendar(
            firstDay: DateTime.utc(2020, 1, 1),
            lastDay: DateTime.utc(2030, 12, 31),
            focusedDay: _focusedDay,
            calendarFormat: _calendarFormat,
            selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
            onDaySelected: (selectedDay, focusedDay) {
              setState(() {
                _selectedDay = selectedDay;
                _focusedDay = focusedDay;
              });
            },
            onFormatChanged: (format) {
              setState(() {
                _calendarFormat = format;
              });
            },
            onPageChanged: (focusedDay) {
              setState(() {
                _focusedDay = focusedDay;
              });
              _loadMealPlans();
            },
            eventLoader: _getMealPlansForDay,
            calendarStyle: const CalendarStyle(
              markersMaxCount: 3,
              markerDecoration: BoxDecoration(
                color: Colors.green,
                shape: BoxShape.circle,
              ),
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: selectedDayPlans.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.restaurant,
                          size: 60,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'No meals planned for this day',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: selectedDayPlans.length,
                    itemBuilder: (context, index) {
                      final mealPlan = selectedDayPlans[index];
                      return Card(
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: _getMealTypeColor(mealPlan.mealType)
                                .withOpacity(0.2),
                            child: Icon(
                              _getMealTypeIcon(mealPlan.mealType),
                              color: _getMealTypeColor(mealPlan.mealType),
                            ),
                          ),
                          title: Text(
                            mealPlan.foodName,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(mealPlan.mealType.toUpperCase()),
                              if (mealPlan.servingSize != null)
                                Text(
                                  'Serving: ${mealPlan.servingSize} ${mealPlan.unitName ?? ''}',
                                ),
                            ],
                          ),
                          trailing: Checkbox(
                            value: mealPlan.isPrepared,
                            onChanged: (value) {
                              mealPlanProvider.togglePreparedStatus(mealPlan.id);
                            },
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(
            context,
            '/meal-plan/add',
            arguments: _selectedDay,
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  IconData _getMealTypeIcon(String mealType) {
    switch (mealType.toLowerCase()) {
      case 'breakfast':
        return Icons.free_breakfast;
      case 'lunch':
        return Icons.lunch_dining;
      case 'dinner':
        return Icons.dinner_dining;
      default:
        return Icons.restaurant;
    }
  }

  Color _getMealTypeColor(String mealType) {
    switch (mealType.toLowerCase()) {
      case 'breakfast':
        return Colors.orange;
      case 'lunch':
        return Colors.blue;
      case 'dinner':
        return Colors.purple;
      default:
        return Colors.green;
    }
  }
}
