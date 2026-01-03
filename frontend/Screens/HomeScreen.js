import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

import FridgeListScreen from './Fridge/FridgeListScreen';
import AddFoodScreen from './Fridge/AddFoodScreen';
import FoodDetailScreen from './Fridge/FoodDetailScreen';
import ShoppingListScreen from './Shopping/ShoppingListScreen';
import ShoppingDetailScreen from './Shopping/ShoppingDetailScreen';
import AddShoppingListScreen from './Shopping/AddShoppingListScreen';
import AddProductScreen from './Shopping/AddProductScreen';
import AddGroupScreen from './Home/AddGroupScreen';
import AddPeopleScreen from './Home/AddPeopleScreen';
import GroupDetailScreen from './Home/GroupDetailScreen';
import ProfileScreen from './ProfileScreen';
import MealPlanScreen from './MealPlan/MealPlanScreen';
import EditMealPlanScreen from './MealPlan/EditMealPlanScreen';

const Tab = createBottomTabNavigator();
const FridgeStack = createNativeStackNavigator();
const ShoppingStack = createNativeStackNavigator();
const HomeStack = createNativeStackNavigator();
const MenuStack = createNativeStackNavigator();

function MenuStackScreen() {
  return (
    <MenuStack.Navigator>
      <MenuStack.Screen 
        name="MealPlanList" 
        component={MealPlanScreen} 
        options={{ headerShown: false }} 
      />
      <MenuStack.Screen 
        name="EditMealPlan" 
        component={EditMealPlanScreen} 
        options={{ headerShown: false }} 
      />
      <MenuStack.Screen
        name="AddMealPlan"
        component={EditMealPlanScreen}
        options={{ headerShown: false }}
      />
    </MenuStack.Navigator>
  );
}

function FridgeStackScreen() {
  return (
    <FridgeStack.Navigator>
      <FridgeStack.Screen
        name="FridgeList"
        component={FridgeListScreen}
        options={{ headerShown: false }}
      />
      <FridgeStack.Screen
        name="AddFood"
        component={AddFoodScreen}
        options={{ title: 'Thêm vào tủ' }}
      />
      <FridgeStack.Screen
        name="FoodDetail"
        component={FoodDetailScreen}
        options={{ headerShown: false }}
      />
    </FridgeStack.Navigator>
  );
}
function ShoppingStackScreen() {
  return (
    <ShoppingStack.Navigator>
      <ShoppingStack.Screen
        name="ShoppingList"
        component={ShoppingListScreen}
        options={{ headerShown: false }}
      /><ShoppingStack.Screen
        name="ShoppingDetail"
        component={ShoppingDetailScreen}
        options={{ title: '' ,
                headerShown: false
        }}
      />
      <ShoppingStack.Screen
        name="AddProduct"
        component={AddProductScreen}
        options={{ title: '',
                headerShown: false
         }}
      />
      <ShoppingStack.Screen
        name="AddShoppingList"
        component={AddShoppingListScreen}
        options={{ headerShown: false }}
      />
    </ShoppingStack.Navigator>
  );
}



function HomeStackScreen() {
  return (
    <HomeStack.Navigator>
      <HomeStack.Screen
        name="GroupDetail"
        component={GroupDetailScreen}
        options={{ headerShown: false }}
      />
      <HomeStack.Screen
        name="AddPeople"
        component={AddPeopleScreen}
        options={{ title: '',
                headerShown: false
         }}
      />
      <HomeStack.Screen
        name="AddGroup"
        component={AddGroupScreen}
        options={{ title: '',
                headerShown: false
         }}
      />
    </HomeStack.Navigator>
  );
}



/* ====== Bottom Tabs ====== */
export default function HomeScreen() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ color, size }) => {
          let iconName;

          switch (route.name) {
            case 'Home':
              iconName = 'home';
              break;
            case 'Fridge':
              iconName = 'cube';
              break;
            case 'Shopping':
              iconName = 'cart';
              break;
            case 'Menu':
              iconName = 'restaurant';
              break;
            case 'Profile':
              iconName = 'person';
              break;
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#4CAF50',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeStackScreen} options={{ title: 'Home' }} />
      <Tab.Screen name="Fridge" component={FridgeStackScreen} options={{ title: 'Tủ lạnh' }} />
      <Tab.Screen name="Shopping" component={ShoppingStackScreen} options={{ title: 'Mua sắm' }} />
      <Tab.Screen name="Menu" component={MenuStackScreen} options={{ title: 'Thực đơn' }} />
      <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: 'Cá nhân' }} />
    </Tab.Navigator>
  );
}

/* ====== Style ====== */
const styles = StyleSheet.create({
  screen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});