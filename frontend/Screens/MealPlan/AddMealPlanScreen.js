import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, ScrollView, TextInput, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import DateTimePicker from '@react-native-community/datetimepicker';

const AddMealPlanScreen = ({ navigation }) => {
  const [mealType, setMealType] = useState('Breakfast');
  const [date, setDate] = useState(new Date());
  const [showPicker, setShowPicker] = useState(false);
  const [foodItems, setFoodItems] = useState([]);

  const addNewFoodInput = () => setFoodItems([...foodItems, '']);
  
  const handleSave = () => {
    // Logic lưu thực đơn mới tại đây
    Alert.alert("Thành công", "Đã tạo thực đơn mới!", [
      { text: "OK", onPress: () => navigation.goBack() }
    ]);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={28} color="black" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Tạo thực đơn mới</Text>
        <View style={{ width: 28 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.label}>Loại bữa ăn</Text>
        <View style={styles.radioGroup}>
          {['Breakfast', 'Lunch', 'Dinner'].map((type) => (
            <TouchableOpacity key={type} style={styles.radioButton} onPress={() => setMealType(type)}>
              <View style={[styles.radioOuter, mealType === type && styles.radioSelected]}>
                {mealType === type && <View style={styles.radioInner} />}
              </View>
              <Text style={styles.radioLabel}>{type}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>Chọn ngày</Text>
        <TouchableOpacity style={styles.datePickerContainer} onPress={() => setShowPicker(true)}>
          <Text>{date.toLocaleDateString('vi-VN')}</Text>
        </TouchableOpacity>

        {showPicker && (
          <DateTimePicker 
            value={date} 
            mode="date" 
            onChange={(e, d) => { setShowPicker(false); if(d) setDate(d); }} 
          />
        )}

        <Text style={styles.label}>Danh sách món ăn</Text>
        {foodItems.map((item, index) => (
          <TextInput 
            key={index}
            style={styles.input}
            placeholder="Nhập tên món..."
            onChangeText={(text) => {
              const newItems = [...foodItems];
              newItems[index] = text;
              setFoodItems(newItems);
            }}
          />
        ))}

        <TouchableOpacity onPress={addNewFoodInput} style={styles.addButton}>
          <Ionicons name="add-circle-outline" size={40} color="#E1AD01" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
          <Text style={styles.saveButtonText}>Lưu thực đơn</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

// Sử dụng chung styles với EditMealPlanScreen của bạn
const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#fff' },
    header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee' },
    headerTitle: { fontSize: 20, fontWeight: 'bold' },
    content: { padding: 20 },
    label: { fontSize: 16, fontWeight: 'bold', marginTop: 20, marginBottom: 10 },
    radioGroup: { flexDirection: 'row', justifyContent: 'space-around' },
    radioButton: { flexDirection: 'row', alignItems: 'center' },
    radioOuter: { width: 20, height: 20, borderRadius: 10, borderWidth: 2, borderColor: '#ccc', justifyContent: 'center', alignItems: 'center', marginRight: 5 },
    radioSelected: { borderColor: '#2ecc71' },
    radioInner: { width: 10, height: 10, borderRadius: 5, backgroundColor: '#2ecc71' },
    datePickerContainer: { padding: 15, borderWidth: 1, borderColor: '#ccc', borderRadius: 10 },
    input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 10, padding: 12, marginBottom: 10 },
    addButton: { alignSelf: 'center', marginVertical: 10 },
    saveButton: { backgroundColor: '#2ecc71', padding: 15, borderRadius: 25, alignItems: 'center', marginTop: 20 },
    saveButtonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 }
});

export default AddMealPlanScreen;