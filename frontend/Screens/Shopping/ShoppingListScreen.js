import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
} from 'react-native';

export default function ShoppingListScreen({ navigation }) {
  const [activities] = useState([
    {
      id: 1,
      title: 'Đi chợ cuối tuần',
      author: 'Nguyễn Văn A',
      level: '5/8 mục',
      date: '06/01',
      progress: 0.625,
      items: [
        { id: '1', name: 'Cà chua', quantity: '2kg', completed: true },
        { id: '2', name: 'Thịt bò', quantity: '1kg', completed: false },
      ]
    },
    {
      id: 2,
      title: 'Mua đồ tiệc',
      author: 'Trần Thị B',
      level: '0/12 mục',
      date: '10/01',
      progress: 0,
    },
  ]);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Mua sắm</Text>
        <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('AddShoppingList')}>
          <Text style={styles.addButtonText}>+</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* Đang hoạt động section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Đang hoạt động ({activities.length})</Text>
          
          {activities.map((activity) => (
            <TouchableOpacity 
              key={activity.id} 
              style={styles.card}
              onPress={() => navigation.navigate('ShoppingDetail', { activity })}>
              <View style={styles.cardContent}>
                <View style={styles.cardLeft}>
                  <View style={styles.cardInfo}>
                    <Text style={styles.cardTitle}>{activity.title}</Text>
                    <Text style={styles.cardSubtitle}>
                      {activity.author} • {activity.level}
                    </Text>
                  </View>
                </View>
                <Text style={styles.cardDate}>{activity.date}</Text>
              </View>
              
              {/* Progress bar */}
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { width: `${activity.progress * 100}%` }
                  ]} 
                />
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  addButton: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addButtonText: {
    fontSize: 28,
    color: '#000',
    fontWeight: '300',
  },
  content: {
    flex: 1,
  },
  section: {
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  cardContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  cardLeft: {
    flexDirection: 'row',
    flex: 1,
  },
  cardIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  cardInfo: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 4,
  },
  cardSubtitle: {
    fontSize: 13,
    color: '#666',
  },
  cardDate: {
    fontSize: 13,
    color: '#999',
  },
  progressBar: {
    height: 4,
    backgroundColor: '#E0E0E0',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
    borderRadius: 2,
  },
  bottomNav: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
    paddingVertical: 8,
    paddingBottom: 20,
  },
  navItem: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 5,
  },
  navItemActive: {
    // Active state
  },
  navIcon: {
    fontSize: 24,
    marginBottom: 4,
  },
  navText: {
    fontSize: 11,
    color: '#666',
  },
  navTextActive: {
    color: '#000',
    fontWeight: '600',
  },
});