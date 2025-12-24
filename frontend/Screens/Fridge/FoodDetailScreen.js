import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  ScrollView, 
  SafeAreaView 
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function FoodDetailScreen({ navigation, route }) {
  // 1. Lấy dữ liệu từ params, nếu không có sẽ gán là {} để tránh lỗi 'undefined'
  const foodItem = route.params?.item || {};

  // 2. Chuẩn bị dữ liệu hiển thị an toàn bằng cách dùng giá trị mặc định
  const displayName = foodItem.name || 'Thực phẩm';
  const displayQuantity = foodItem.quantity || 'Chưa rõ số lượng';
  const displayExpiry = foodItem.expiryDate || 'Chưa cập nhật';
  const displayDays = foodItem.daysLeft !== undefined ? ` (Còn ${foodItem.daysLeft} ngày)` : '';
  const displayLocation = foodItem.location || 'Chưa rõ vị trí';
  const displayNote = foodItem.note || 'Không có ghi chú';
  
  // Kiểm tra danh sách món ăn gợi ý, nếu không có sẽ gán mảng trống []
  const displayMeals = foodItem.suggestedMeals || [];

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="chevron-back" size={28} color="black" />
        </TouchableOpacity>
        
        {/* Hiển thị tên động an toàn */}
        <Text style={styles.headerTitle}>{displayName}</Text>
        
        <TouchableOpacity>
          <Ionicons name="pencil-outline" size={24} color="black" />
        </TouchableOpacity>
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.content}>
        {/* Khu vực hình ảnh thực phẩm */}
        <View style={styles.imagePlaceholder}>
          <Text style={styles.placeholderText}>Hình ảnh thực phẩm</Text>
        </View>

        {/* Bảng thông tin chi tiết */}
        <View style={styles.infoCard}>
          <View style={styles.infoRow}>
            <View style={styles.infoLabelGroup}>
              <Text style={styles.icon}>📦</Text>
              <Text style={styles.label}>Số lượng</Text>
            </View>
            <Text style={styles.value}>{displayQuantity}</Text>
          </View>

          <View style={styles.infoRow}>
            <View style={styles.infoLabelGroup}>
              <Text style={styles.icon}>⏰</Text>
              <Text style={styles.label}>Hạn dùng</Text>
            </View>
            <Text style={[styles.value, styles.expiryValue]}>
              {displayExpiry}{displayDays}
            </Text>
          </View>

          <View style={styles.infoRow}>
            <View style={styles.infoLabelGroup}>
              <Text style={styles.icon}>📍</Text>
              <Text style={styles.label}>Vị trí</Text>
            </View>
            <Text style={styles.value}>{displayLocation}</Text>
          </View>

          <View style={styles.infoRow}>
            <View style={styles.infoLabelGroup}>
              <Text style={styles.icon}>📝</Text>
              <Text style={styles.label}>Ghi chú</Text>
            </View>
            <Text style={styles.value}>{displayNote}</Text>
          </View>
        </View>

        {/* Các nút chức năng */}
        <View style={styles.buttonRow}>
          <TouchableOpacity style={styles.actionButton}>
            <Text style={styles.actionButtonText}>Đã dùng hết</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.actionButton, styles.buyButton]}>
            <Text style={styles.actionButtonText}>Thêm vào DS mua</Text>
          </TouchableOpacity>
        </View>

        {/* Gợi ý món ăn - SỬA LỖI .MAP() TẠI ĐÂY */}
        <View style={styles.suggestionSection}>
          <Text style={styles.sectionTitle}>Gợi ý món ăn:</Text>
          
          {displayMeals.length > 0 ? (
            displayMeals.map((meal, index) => (
              <View key={index} style={styles.mealItem}>
                <Text style={styles.mealText}>{meal}</Text>
              </View>
            ))
          ) : (
            <Text style={styles.emptyText}>Chưa có gợi ý món ăn cho thực phẩm này.</Text>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  headerTitle: { fontSize: 20, fontWeight: 'bold' },
  content: { padding: 16 },
  imagePlaceholder: {
    width: '100%',
    height: 200,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#ddd',
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  placeholderText: { color: '#999' },
  infoCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 0.5,
    borderBottomColor: '#f0f0f0',
  },
  infoLabelGroup: { flexDirection: 'row', alignItems: 'center' },
  icon: { fontSize: 18, marginRight: 8 },
  label: { fontSize: 16, color: '#666' },
  value: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  expiryValue: { color: '#FF4D4D' }, 
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  actionButton: {
    flex: 0.48,
    paddingVertical: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#333',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  buyButton: {
    backgroundColor: '#f0f0f0',
    borderColor: '#f0f0f0',
  },
  actionButtonText: { fontSize: 14, fontWeight: 'bold', color: '#333' },
  suggestionSection: { marginTop: 10, paddingBottom: 30 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 12, color: '#333' },
  mealItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  mealText: { fontSize: 16, color: '#444' },
  emptyText: { color: '#999', fontStyle: 'italic' }
});