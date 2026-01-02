import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const MEAL_PLANS = [
  { id: '1', title: 'This Morning' },
  { id: '2', title: 'Yesterday Evening' },
  { id: '3', title: 'Yesterday Lunch' },
  { id: '4', title: 'Nov 21st Evening' },
  { id: '5', title: 'Nov 21st Lunch' },
];

const MealPlanScreen = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={28} color="#2c3e50" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Danh sách thực đơn</Text>
        <View style={{ width: 28 }} /> 
      </View>

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        {/* Render danh sách các thực đơn */}
        {MEAL_PLANS.map((item) => (
          <View key={item.id} style={styles.mealCard}>
            <Text style={styles.mealTitle}>{item.title}</Text>
            
            <View style={styles.actionGroup}>
              <TouchableOpacity style={styles.iconButton} onPress={() => navigation.navigate('EditMealPlan', { mealTitle: item.title })}>
                <Ionicons name="create-outline" size={24} color="#2ecc71" />
              </TouchableOpacity>
              <TouchableOpacity style={styles.iconButton}>
                <Ionicons name="trash-outline" size={24} color="#e74c3c" />
              </TouchableOpacity>
            </View>
          </View>
        ))}
      </ScrollView>

      <TouchableOpacity 
        style={styles.fab} 
        onPress={() => navigation.navigate('AddMealPlan')}
      >
        <Ionicons name="add" size={35} color="#E1AD01" />
      </TouchableOpacity>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  content: {
    padding: 20,
    paddingBottom: 100, // Chừa khoảng trống cho nút FAB
  },
  mealCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#7f8c8d',
    borderRadius: 15,
    paddingVertical: 15,
    paddingHorizontal: 20,
    marginBottom: 15,
  },
  mealTitle: {
    fontSize: 18,
    color: '#2c3e50',
    flex: 1,
  },
  actionGroup: {
    flexDirection: 'row',
  },
  iconButton: {
    marginLeft: 15,
  },
  fab: {
    position: 'absolute',
    right: 30,
    bottom: 30,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5, // Đổ bóng cho Android
    shadowColor: '#000', // Đổ bóng cho iOS
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    borderWidth: 2,
    borderColor: '#f39c12',
  },
});

export default MealPlanScreen;