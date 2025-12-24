import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  ScrollView, 
  KeyboardAvoidingView, 
  Platform 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Dropdown } from 'react-native-element-dropdown';
import DateTimePicker from '@react-native-community/datetimepicker';

export default function AddFoodScreen({ navigation }) {
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [unit, setUnit] = useState('kg');
  const [location, setLocation] = useState('Ngăn mát');
  const [note, setNote] = useState('');

  const [isFocus, setIsFocus] = useState(false);

  // --- State quản lý ngày tháng (Date Picker) ---
  const [date, setDate] = useState(new Date()); // Lưu đối tượng ngày thực tế
  const [showDatePicker, setShowDatePicker] = useState(false); // Đóng/mở lịch

  const unitData = [
    { label: 'kg', value: 'kg' },
    { label: 'hộp', value: 'hộp' },
    { label: 'túi', value: 'túi' },
    { label: 'lít', value: 'lít' },
    { label: 'quả', value: 'quả' },
  ];

  // Hàm xử lý khi chọn ngày xong
  const onDateChange = (event, selectedDate) => {
    setShowDatePicker(false); // Luôn đóng lịch sau khi tương tác
    if (selectedDate) {
      setDate(selectedDate); // Cập nhật ngày mới
    }
  };

  // Hàm định dạng hiển thị ngày DD/MM/YYYY
  const formatDateDisplay = (date) => {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>
        
        {/* Tên thực phẩm */}
        <Text style={styles.label}>Tên thực phẩm *</Text>
        <View style={styles.inputContainer}>
          <TextInput 
            style={styles.input} 
            placeholder="Cà chua" 
            value={name} 
            onChangeText={setName} 
          />
          <Ionicons name="search" size={20} color="#999" style={styles.inputIcon} />
        </View>

        {/* Số lượng & Đơn vị */}
        <View style={styles.row}>
          <View style={{ flex: 1, marginRight: 10 }}>
            <Text style={styles.label}>Số lượng *</Text>
            <TextInput 
              style={styles.input} 
              placeholder="2.5" 
              keyboardType="numeric"
              value={quantity} 
              onChangeText={setQuantity} 
            />
          </View>
          <View style={{ flex: 1 }}>
            <Text style={styles.label}>Đơn vị</Text>
            <View style={styles.pickerWrapper}>
              <Dropdown
              style={[styles.dropdown, isFocus && { borderColor: '#4CAF50' }]}
              placeholderStyle={styles.placeholderStyle}
              selectedTextStyle={styles.selectedTextStyle}
              data={unitData}
              maxHeight={200}
              labelField="label"
              valueField="value"
              placeholder={!isFocus ? 'Chọn' : '...'}
              value={unit}
              onFocus={() => setIsFocus(true)}
              onBlur={() => setIsFocus(false)}
              onChange={item => {
                setUnit(item.value);
                setIsFocus(false);
              }}
              // Vẽ icon tam giác ở bên phải
              renderRightIcon={() => (
                <Ionicons 
                  name="caret-down" 
                  size={14} 
                  color={isFocus ? '#4CAF50' : '#999'} 
                />
              )}
            />
            </View>
          </View>
        </View>

{/* Hạn sử dụng - Tích hợp DatePicker */}
        <Text style={styles.label}>Hạn sử dụng *</Text>
        <TouchableOpacity 
          style={styles.inputContainer} 
          onPress={() => setShowDatePicker(true)}
        >
          <Ionicons name="calendar-outline" size={20} color="#666" style={{ marginLeft: 10 }} />
          <TextInput 
            style={[styles.input, { color: '#333' }]} 
            value={formatDateDisplay(date)} 
            editable={false} // Bắt buộc chọn qua lịch
          />
        </TouchableOpacity>

        {showDatePicker && (
          <DateTimePicker
            value={date}
            mode="date"
            display={Platform.OS === 'android' ? 'calendar' : 'spinner'} 
            onChange={onDateChange}
          />
        )}

        {/* Vị trí */}
        <Text style={styles.label}>Vị trí</Text>
        <View style={styles.locationRow}>
          {['Ngăn mát', 'Ngăn đông'].map((item) => (
            <TouchableOpacity 
              key={item}
              style={[styles.locationTab, location === item && styles.locationTabActive]}
              onPress={() => setLocation(item)}
            >
              <Text style={[styles.locationTabText, location === item && styles.locationTabTextActive]}>
                {item}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Ghi chú */}
        <Text style={styles.label}>Ghi chú</Text>
        <TextInput 
          style={[styles.input, styles.textArea]} 
          placeholder="Nhập ghi chú thêm về thực phẩm..." 
          multiline={true}
          numberOfLines={3}
          value={note}
          onChangeText={setNote}
        />

        {/* Nút lưu */}
        <TouchableOpacity
          style={styles.saveButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.saveButtonText}>Lưu vào tủ lạnh</Text>
        </TouchableOpacity>

      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingBottom: 10,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  headerTitle: { fontSize: 18, fontWeight: 'bold' },
  scrollContent: { padding: 16 },
  label: { fontSize: 14, fontWeight: '600', marginBottom: 8, marginTop: 15, color: '#333' },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  input: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 12,
    fontSize: 16,
  },
  inputIcon: { marginRight: 12 },
  row: { flexDirection: 'row' },
  locationRow: { flexDirection: 'row', marginTop: 5 },
  locationTab: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 6,
    backgroundColor: '#f0f0f0',
    marginRight: 10,
  },
  locationTabActive: { backgroundColor: '#333' },
  locationTabText: { color: '#333' },
  locationTabTextActive: { color: '#fff', fontWeight: 'bold' },
  textArea: {
    height: 80,
    textAlignVertical: 'top',
    paddingTop: 12,
  },
  saveButton: {
    backgroundColor: '#333',
    paddingVertical: 16,
    alignItems: 'center',
    borderRadius: 12,
    marginTop: 30,
    marginBottom: 50,
  },
  saveButtonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
});