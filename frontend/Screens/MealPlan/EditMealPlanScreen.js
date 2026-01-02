import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  Platform, 
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import DateTimePicker from '@react-native-community/datetimepicker';

const EditMealPlanScreen = ({ navigation }) => {
  const [mealType, setMealType] = useState('Breakfast');
  
  // State quản lý ngày chọn (dạng đối tượng Date)
  const [date, setDate] = useState(new Date()); // Mặc định 24/01/2026
  const [showPicker, setShowPicker] = useState(false);

  // Hàm xử lý khi thay đổi ngày trên lịch
  const onChange = (event, selectedDate) => {
    const currentDate = selectedDate || date;
    setShowPicker(Platform.OS === 'ios');
    setDate(currentDate);
  };

  // Hàm định dạng ngày để hiển thị vào ô (DD/MM/YYYY)
  const formatDate = (date) => {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  const [foodItems, setFoodItems] = useState([]);
  const addNewFoodInput = () => setFoodItems([...foodItems, '']);
  const updateFoodItem = (text, index) => {
    const newItems = [...foodItems];
    newItems[index] = text;
    setFoodItems(newItems);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={28} color="black" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Chỉnh sửa thực đơn</Text>
        <View style={{ width: 28 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* Type of meal */}
        <Text style={styles.label}>Bữa ăn</Text>
        <View style={styles.radioGroup}>
          {['Sáng', 'Trưa', 'Tối'].map((type) => (
            <TouchableOpacity key={type} style={styles.radioButton} onPress={() => setMealType(type)}>
              <View style={[styles.radioOuter, mealType === type && styles.radioSelected]}>
                {mealType === type && <View style={styles.radioInner} />}
              </View>
              <Text style={styles.radioLabel}>{type}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <Text style={styles.label}>Chọn ngày</Text>
        <TouchableOpacity 
          style={styles.datePickerContainer} 
          onPress={() => setShowPicker(true)}
        >
          <View style={styles.dateDisplay}>
            <Ionicons name="calendar-outline" size={20} color="#666" style={styles.calendarIcon} />
            <Text style={styles.dateText}>{formatDate(date)}</Text>
          </View>
        </TouchableOpacity>

        {/* Giao diện Lịch hiện lên khi nhấn vào ô */}
        {showPicker && (
          <DateTimePicker
            value={date}
            mode="date"
            display="default"
            onChange={onChange}
          />
        )}
        {/* -------------------------------- */}

        {/* Food list */}
        <Text style={styles.label}>Danh sách món</Text>
        {foodItems.map((item, index) => (
          <View key={index} style={styles.foodInputWrapper}>
            <TextInput
              style={styles.foodTextInput}
              value={item}
              placeholder="Nhập tên món ăn..."
              onChangeText={(text) => updateFoodItem(text, index)}
            />
            <TouchableOpacity onPress={() => {
              const newItems = foodItems.filter((_, i) => i !== index);
              setFoodItems(newItems);
            }}>
              <Ionicons name="trash-outline" size={24} color="#e74c3c" />
            </TouchableOpacity>
          </View>
        ))}

        <TouchableOpacity style={styles.addIconButton} onPress={addNewFoodInput}>
          <Ionicons name="add-circle-outline" size={45} color="#E1AD01" />
        </TouchableOpacity>

        <TouchableOpacity style={styles.saveButton}>
          <Text style={styles.saveButtonText}>Lưu</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee' },
  headerTitle: { fontSize: 20, fontWeight: 'bold' },
  content: { padding: 20, paddingBottom: 50 },
  label: { fontSize: 18, fontWeight: '600', marginTop: 25, marginBottom: 10 },
  
  // Style cho ô chọn ngày mới
  datePickerContainer: {
    height: 55,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 12,
    justifyContent: 'center',
    paddingHorizontal: 15,
    backgroundColor: '#fff',
  },
  dateDisplay: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  calendarIcon: {
    marginRight: 10,
  },
  dateText: {
    fontSize: 16,
    color: '#333',
  },

  // Radio button & Food list styles (giữ lại từ bản trước)
  radioGroup: { flexDirection: 'row', justifyContent: 'space-between' },
  radioButton: { flexDirection: 'row', alignItems: 'center' },
  radioOuter: { width: 22, height: 22, borderRadius: 11, borderWidth: 2, borderColor: '#ccc', justifyContent: 'center', alignItems: 'center', marginRight: 8 },
  radioSelected: { borderColor: '#2ecc71' },
  radioInner: { width: 12, height: 12, borderRadius: 6, backgroundColor: '#2ecc71' },
  radioLabel: { fontSize: 16 },
  foodInputWrapper: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 15, borderWidth: 1, borderColor: '#bdc3c7', borderRadius: 10, paddingHorizontal: 15, height: 50 },
  foodTextInput: { flex: 1, fontSize: 16 },
  addIconButton: { alignSelf: 'center', marginTop: 10, marginBottom: 30 },
  saveButton: { backgroundColor: '#2ecc71', height: 55, borderRadius: 30, justifyContent: 'center', alignItems: 'center' },
  saveButtonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' }
});

export default EditMealPlanScreen;