import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function AddItemScreen({ navigation }) {
  const [itemName, setItemName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [unit, setUnit] = useState('quả');

  const units = ['quả', 'kg', 'gói', 'hộp', 'chai', 'lon', 'cái'];

  const handleAddItem = () => {
    if (!itemName.trim()) {
      Alert.alert('Lỗi', 'Vui lòng nhập tên món');
      return;
    }

    if (!quantity.trim()) {
      Alert.alert('Lỗi', 'Vui lòng nhập số lượng');
      return;
    }

    Alert.alert(
      'Thành công',
      `Đã thêm: ${quantity} ${unit} ${itemName}`,
      [
        {
          text: 'OK',
          onPress: () => {
            // Reset form
            setItemName('');
            setQuantity('');
            setUnit('quả');
          }
        }
      ]
    );
  };

  const [showUnitPicker, setShowUnitPicker] = useState(false);

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => navigation?.goBack()}
        >
          <Ionicons name="chevron-back" size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Thêm mục</Text>
        <View style={styles.headerRight} />
      </View>

      <ScrollView style={styles.scrollView}>
        <View style={styles.content}>
          {/* Nhập thủ công Section */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Nhập thủ công</Text>

            {/* Tên món */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Tên món</Text>
              <TextInput
                style={styles.input}
                value={itemName}
                onChangeText={setItemName}
                placeholder="Trứng gà"
                placeholderTextColor="#999"
              />
            </View>

            {/* Số lượng và Đơn vị */}
            <View style={styles.row}>
              {/* Số lượng */}
              <View style={styles.halfInput}>
                <Text style={styles.label}>Số lượng</Text>
                <TextInput
                  style={styles.input}
                  value={quantity}
                  onChangeText={setQuantity}
                  placeholder="10"
                  placeholderTextColor="#999"
                  keyboardType="numeric"
                />
              </View>

              {/* Đơn vị */}
              <View style={styles.halfInput}>
                <Text style={styles.label}>Đơn vị</Text>
                <TouchableOpacity 
                  style={styles.dropdownInput}
                  onPress={() => setShowUnitPicker(!showUnitPicker)}
                >
                  <Text style={styles.dropdownText}>{unit}</Text>
                  <Ionicons name="chevron-down" size={20} color="#666" />
                </TouchableOpacity>
              </View>
            </View>

            {/* Unit Picker */}
            {showUnitPicker && (
              <View style={styles.unitPicker}>
                {units.map((u) => (
                  <TouchableOpacity
                    key={u}
                    style={styles.unitOption}
                    onPress={() => {
                      setUnit(u);
                      setShowUnitPicker(false);
                    }}
                  >
                    <Text style={[
                      styles.unitOptionText,
                      u === unit && styles.unitOptionTextActive
                    ]}>
                      {u}
                    </Text>
                    {u === unit && (
                      <Ionicons name="checkmark" size={20} color="#007AFF" />
                    )}
                  </TouchableOpacity>
                ))}
              </View>
            )}

            {/* Submit Button */}
            <TouchableOpacity 
              style={styles.submitButton}
              onPress={handleAddItem}
              activeOpacity={0.8}
            >
              <Text style={styles.submitButtonText}>Thêm vào danh sách</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  backButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000',
  },
  headerRight: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 16,
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#000',
    marginBottom: 20,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#d1d1d6',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 15,
    color: '#000',
    backgroundColor: '#fff',
  },
  row: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 20,
  },
  halfInput: {
    flex: 1,
  },
  dropdownInput: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderColor: '#d1d1d6',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 14,
    backgroundColor: '#fff',
  },
  dropdownText: {
    fontSize: 15,
    color: '#000',
  },
  unitPicker: {
    borderWidth: 1,
    borderColor: '#d1d1d6',
    borderRadius: 8,
    backgroundColor: '#fff',
    marginBottom: 20,
    maxHeight: 200,
  },
  unitOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  unitOptionText: {
    fontSize: 15,
    color: '#000',
  },
  unitOptionTextActive: {
    color: '#007AFF',
    fontWeight: '600',
  },
  submitButton: {
    backgroundColor: '#1c1c1e',
    borderRadius: 8,
    paddingVertical: 16,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});