import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
} from 'react-native';

export default function DetailScreen({ navigation, route }) {
  const { activity } = route.params;
  const [items, setItems] = useState(activity.items);

  const toggleItem = (itemId) => {
    setItems(items.map(item => 
      item.id === itemId ? { ...item, completed: !item.completed } : item
    ));
  };

  // const completedCount = items.filter(item => item.completed).length;

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* Header */}
      <View style={styles.detailHeader}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>{'<'}</Text>
        </TouchableOpacity>
        <Text style={styles.detailHeaderTitle}>{activity.title}</Text>
        <TouchableOpacity>
          <Text style={styles.menuButton}>⋮</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.detailContent}>
        {/* Budget Info */}
        <View style={styles.budgetCard}>
          <View style={styles.budgetRow}>
            <View>
              <Text style={styles.budgetLabel}>Ngân sách: {activity.budget}</Text>
              <Text style={styles.budgetLabel}>Thực tế: {activity.spent}</Text>
            </View>
            <View style={styles.statusBadge}>
              {/* <Text style={styles.statusText}>{completedCount}/{items.length}</Text> */}
              <Text style={styles.statusLabel}>Hoàn thành</Text>
            </View>
          </View>
        </View>

        {/* Add Item Button */}
        <TouchableOpacity style={styles.addItemButton}
          onPress={() => navigation.navigate('AddProduct', { activityId: activity.id })}
        >
          <Text style={styles.addItemText}>+ Thêm mục</Text>
        </TouchableOpacity>

        {/* Items List */}
        <View style={styles.itemsList}>
          {items.map((item) => (
            <View key={item.id} style={styles.itemRow}>
              <TouchableOpacity 
                style={styles.checkbox}
                onPress={() => toggleItem(item.id)}
              >
                {item.completed && (
                  <View style={styles.checkboxChecked}>
                    <Text style={styles.checkmark}>✓</Text>
                  </View>
                )}
              </TouchableOpacity>
              
              <View style={styles.itemInfo}>
                <Text style={[
                  styles.itemName,
                  item.completed && styles.itemNameCompleted
                ]}>
                  {item.name}
                </Text>
                <Text style={styles.itemPrice}>
                  {item.price}
                  {item.estimatedPrice && ` • Thực tế: ${item.estimatedPrice}`}
                </Text>
              </View>
              
              <TouchableOpacity>
                <Text style={styles.itemMenu}>⋮</Text>
              </TouchableOpacity>
            </View>
          ))}
        </View>
      </ScrollView>

      {/* Complete Button */}
      <View style={styles.bottomButton}>
        <TouchableOpacity style={styles.completeButton}>
          <Text style={styles.completeButtonText}>Hoàn thành mua sắm</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  detailHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  backButton: {
    fontSize: 24,
    color: '#000',
  },
  detailHeaderTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  menuButton: {
    fontSize: 24,
    color: '#000',
  },
  detailContent: {
    flex: 1,
    padding: 20,
  },
  budgetCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
  },
  budgetRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  budgetLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  statusBadge: {
    alignItems: 'flex-end',
  },
  statusText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statusLabel: {
    fontSize: 12,
    color: '#666',
  },
  addItemButton: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: '#CCCCCC',
    alignItems: 'center',
  },
  addItemText: {
    fontSize: 16,
    color: '#666',
  },
  itemsList: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 10,
  },
  itemRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderWidth: 2,
    borderColor: '#CCCCCC',
    borderRadius: 4,
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    width: '100%',
    height: '100%',
    backgroundColor: '#4CAF50',
    borderRadius: 2,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmark: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: 'bold',
  },
  itemInfo: {
    flex: 1,
  },
  itemName: {
    fontSize: 16,
    color: '#000',
    marginBottom: 4,
  },
  itemNameCompleted: {
    textDecorationLine: 'line-through',
    color: '#999',
  },
  itemPrice: {
    fontSize: 13,
    color: '#666',
  },
  itemMenu: {
    fontSize: 20,
    color: '#999',
  },
  bottomButton: {
    padding: 20,
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
  },
  completeButton: {
    backgroundColor: '#333333',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  completeButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});