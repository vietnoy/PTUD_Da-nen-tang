import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'providers/auth_provider.dart';
import 'providers/fridge_provider.dart';
import 'providers/shopping_provider.dart';
import 'providers/meal_plan_provider.dart';
import 'providers/food_provider.dart';

import 'screens/auth/login_screen.dart';
import 'screens/auth/register_screen.dart';
import 'screens/auth/verify_email_screen.dart';
import 'screens/home_screen.dart';
import 'screens/fridge/add_fridge_item_screen.dart';
import 'screens/group/group_screen.dart';
import 'screens/food/food_list_screen.dart';
import 'screens/food/add_food_screen.dart';
import 'screens/profile/edit_profile_screen.dart';
import 'screens/profile/change_password_screen.dart';
import 'screens/shopping/create_shopping_list_screen.dart';
import 'screens/meal_plan/add_meal_plan_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => FridgeProvider()),
        ChangeNotifierProvider(create: (_) => ShoppingProvider()),
        ChangeNotifierProvider(create: (_) => MealPlanProvider()),
        ChangeNotifierProvider(create: (_) => FoodProvider()),
      ],
      child: Consumer<AuthProvider>(
        builder: (context, authProvider, _) {
          return MaterialApp(
            title: 'Di Cho Tien Loi',
            debugShowCheckedModeBanner: false,
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: Colors.green,
                brightness: Brightness.light,
              ),
              useMaterial3: true,
              appBarTheme: const AppBarTheme(
                centerTitle: true,
                elevation: 0,
              ),
            ),
            home: authProvider.isLoading
                ? const Scaffold(
                    body: Center(
                      child: CircularProgressIndicator(),
                    ),
                  )
                : authProvider.isAuthenticated
                    ? const HomeScreen()
                    : const LoginScreen(),
            onGenerateRoute: (settings) {
              // Auth routes
              if (settings.name == '/login') {
                return MaterialPageRoute(builder: (_) => const LoginScreen());
              }
              if (settings.name == '/register') {
                return MaterialPageRoute(builder: (_) => const RegisterScreen());
              }
              if (settings.name == '/verify-email') {
                final email = settings.arguments as String;
                return MaterialPageRoute(
                  builder: (_) => VerifyEmailScreen(email: email),
                );
              }

              // Protected routes - require authentication
              if (!authProvider.isAuthenticated) {
                return MaterialPageRoute(builder: (_) => const LoginScreen());
              }

              // Home
              if (settings.name == '/home') {
                return MaterialPageRoute(builder: (_) => const HomeScreen());
              }

              // Fridge routes
              if (settings.name == '/fridge/add') {
                return MaterialPageRoute(builder: (_) => const AddFridgeItemScreen());
              }

              // Group routes
              if (settings.name == '/group') {
                final authProvider = Provider.of<AuthProvider>(context, listen: false);
                final groupId = authProvider.groupId;
                if (groupId == null) {
                  return MaterialPageRoute(
                    builder: (_) => Scaffold(
                      appBar: AppBar(title: const Text('Group')),
                      body: const Center(
                        child: Text('You are not part of any group'),
                      ),
                    ),
                  );
                }
                return MaterialPageRoute(builder: (_) => GroupScreen(groupId: groupId));
              }

              // Food routes
              if (settings.name == '/food') {
                return MaterialPageRoute(builder: (_) => const FoodListScreen());
              }

              // Profile routes
              if (settings.name == '/profile/edit') {
                return MaterialPageRoute(builder: (_) => const EditProfileScreen());
              }
              if (settings.name == '/profile/change-password') {
                return MaterialPageRoute(builder: (_) => const ChangePasswordScreen());
              }

              // Food routes
              if (settings.name == '/food/add') {
                return MaterialPageRoute(builder: (_) => const AddFoodScreen());
              }

              // Shopping routes
              if (settings.name == '/shopping/create') {
                return MaterialPageRoute(builder: (_) => const CreateShoppingListScreen());
              }

              // Meal plan routes
              if (settings.name == '/meal-plan/add') {
                final date = settings.arguments as DateTime?;
                return MaterialPageRoute(builder: (_) => AddMealPlanScreen(selectedDate: date));
              }

              // TODO: Add more routes for other screens
              // Fridge routes: /fridge/edit
              // Shopping routes: /shopping/create, /shopping/details, /shopping/add-tasks
              // Meal plan routes: /meal-plan/add, /meal-plan/edit
              // Profile routes: /profile/edit, /profile/change-password
              // Food routes: /food/add, /food/edit

              return null;
            },
          );
        },
      ),
    );
  }
}
