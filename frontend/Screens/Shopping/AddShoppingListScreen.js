import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Platform,
  Alert
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function NewListScreen({ navigation }) {
  const [listName, setListName] = useState('');
  const [assignedTo, setAssignedTo] = useState('Nguyễn Văn A');
  const [dueDate, setDueDate] = useState('06/01/2025');
  const [estimatedBudget, setEstimatedBudget] = useState('500,000 VND');

  const handleSubmit = () => {
    if (!listName.trim()) {
      Alert.alert('Lỗi', 'Vui lòng nhập tên danh sách');
      return;
    }

    Alert.alert(
      'Thành công',
      'Danh sách đã được tạo!',
      [
        {
          text: 'OK',
          onPress: () => {
            // Reset form hoặc navigate back
            setListName('');
          }
        }
      ]
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => navigation?.goBack()}
        >
          <Ionicons name="chevron-back" size={24} color="#000" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Danh sách mới</Text>
        <View style={styles.headerRight} />
      </View>

      <ScrollView style={styles.scrollView}>
        <View style={styles.form}>
          {/* Tên danh sách */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>
              Tên danh sách <Text style={styles.required}>*</Text>
            </Text>
            <TextInput
              style={styles.input}
              value={listName}
              onChangeText={setListName}
              placeholder="Đi chợ cuối tuần"
              placeholderTextColor="#999"
            />
          </View>

          {/* Phân công cho */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Phân công cho</Text>
            <TouchableOpacity style={styles.dropdownInput}>
              <Text style={styles.dropdownText}>{assignedTo} ▼</Text>
            </TouchableOpacity>
          </View>

          {/* Hạn hoàn thành */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Hạn hoàn thành</Text>
            <TouchableOpacity style={styles.dateInput}>
              <Text style={styles.emoji}>📅</Text>
              <Text style={styles.dateText}>{dueDate}</Text>
            </TouchableOpacity>
          </View>

          {/* Ngân sách dự kiến */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Ngân sách dự kiến</Text>
            <TextInput
              style={styles.input}
              value={estimatedBudget}
              onChangeText={setEstimatedBudget}
              placeholder="500,000 VND"
              placeholderTextColor="#999"
              keyboardType="numeric"
            />
          </View>

          {/* Submit Button */}
          <TouchableOpacity 
            style={styles.submitButton}
            onPress={handleSubmit}
            activeOpacity={0.8}
          >
            <Text style={styles.submitButtonText}>Tạo danh sách</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
}

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
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
    backgroundColor: '#fff',
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
  form: {
    padding: 20,
  },
  inputGroup: {
    marginBottom: 24,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    marginBottom: 8,
  },
  required: {
    color: '#ff3b30',
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
  dropdownInput: {
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
  dateInput: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#d1d1d6',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 14,
    backgroundColor: '#fff',
  },
  emoji: {
    fontSize: 20,
    marginRight: 10,
  },
  dateText: {
    fontSize: 15,
    color: '#000',
  },
  submitButton: {
    backgroundColor: '#1c1c1e',
    borderRadius: 8,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 16,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});