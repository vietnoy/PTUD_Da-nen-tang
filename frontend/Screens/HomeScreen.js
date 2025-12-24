import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

/* ====== Các màn hình TRỐNG ====== */
function HomeTab() {
  return (
    <View style={styles.screen}>
      <Text>Home</Text>
    </View>
  );
}

function FridgeTab() {
  return (
    <View style={styles.screen}>
      <Text>Tủ lạnh</Text>
    </View>
  );
}

function ShoppingTab() {
  return (
    <View style={styles.screen}>
      <Text>Mua sắm</Text>
    </View>
  );
}

function MenuTab() {
  return (
    <View style={styles.screen}>
      <Text>Thực đơn</Text>
    </View>
  );
}

function ProfileTab() {
  return (
    <View style={styles.screen}>
      <Text>Cá nhân</Text>
    </View>
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
      <Tab.Screen name="Home" component={HomeTab} options={{ title: 'Home' }} />
      <Tab.Screen name="Fridge" component={FridgeTab} options={{ title: 'Tủ lạnh' }} />
      <Tab.Screen name="Shopping" component={ShoppingTab} options={{ title: 'Mua sắm' }} />
      <Tab.Screen name="Menu" component={MenuTab} options={{ title: 'Thực đơn' }} />
      <Tab.Screen name="Profile" component={ProfileTab} options={{ title: 'Cá nhân' }} />
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
