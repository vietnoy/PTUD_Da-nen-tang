import React, { useState } from 'react';
import { View, Text, TouchableOpacity, FlatList, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const DATA = [
  { id: '1', name: 'Cà chua', quantity: '2.5kg', daysLeft: 2, location: 'Ngăn mát' },
  { id: '2', name: 'Sữa tươi', quantity: '1 hộp', daysLeft: 1, location: 'Ngăn mát' },
  { id: '3', name: 'Thịt heo', quantity: '1.5kg', daysLeft: 5, location: 'Ngăn đông' },
  { id: '4', name: 'Cà rốt', quantity: '1kg', daysLeft: 7, location: 'Ngăn mát' },
];

export default function FridgeListScreen({ navigation }) {
  const [filter, setFilter] = useState('all');

  /* ===== LỌC ===== */
  const filteredData = DATA.filter(item => {
    if (filter === 'EXPIRING') return item.daysLeft <= 3;
    if (filter === 'FREEZER') return item.location === 'Ngăn đông';
    if (filter === 'COOL') return item.location === 'Ngăn mát';
    return true;
  });

  const warning = filteredData.filter(i => i.daysLeft <= 3);
  const good = filteredData.filter(i => i.daysLeft > 3);

  /* ===== ITEM ===== */
  const renderItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.item}
      onPress={() => navigation.navigate('FoodDetail', { item })} 
    >
      <View style={styles.image}>
         <Ionicons name="nutrition-outline" size={20} color="#ccc" />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.name}>{item.name}</Text>
        <Text style={styles.sub}>
          {item.quantity} • Còn {item.daysLeft} ngày
        </Text>
      </View>
      <Ionicons name="chevron-forward" size={18} color="gray" />
    </TouchableOpacity>
  );
 
   return (
    <View style={styles.container}>
      {/* HEADER */}
      <View style={styles.header}>
        <Text style={styles.title}>Tủ lạnh</Text>
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <Ionicons name="search" size={22} />
          <TouchableOpacity onPress={() => navigation.navigate('AddFood')}>
            <Ionicons name="add" size={30} color="#4CAF50" style={{ marginLeft: 12 }} />
          </TouchableOpacity>
        </View>
      </View>
 
       {/* FILTER */}
       <View style={styles.filterRow}>
         <FilterButton label="Tất cả" active={filter === 'ALL'} onPress={() => setFilter('ALL')} />
         <FilterButton label="Sắp hết hạn" active={filter === 'EXPIRING'} onPress={() => setFilter('EXPIRING')} />
         <FilterButton label="Ngăn đông" active={filter === 'FREEZER'} onPress={() => setFilter('FREEZER')} />
         <FilterButton label="Ngăn mát" active={filter === 'COOL'} onPress={() => setFilter('COOL')} />
       </View>
 
       {/* WARNING */}
       {warning.length > 0 && (
         <>
           <Text stylel={styles.sectionWarning}>⚠ Cần chú ý</Text>
           <FlatList data={warning} renderItem={renderItem} keyExtractor={i => i.id} />
         </>
       )}
 
       {/* GOOD */}
       {good.length > 0 && (
         <>
           <Text style={styles.section}>Còn tốt</Text>
           <FlatList data={good} renderItem={renderItem} keyExtractor={i => i.id} />
         </>
       )}
     </View>
   );
 }
 
 /* ===== FILTER BUTTON ===== */
 const FilterButton = ({ label, active, onPress }) => (
   <TouchableOpacity
     style={[styles.filterBtn, active && styles.filterActive]}
     onPress={onPress}
   >
     <Text style={{ color: active ? '#fff' : '#000' }}>{label}</Text>
   </TouchableOpacity>
 );
 
 /* ===== STYLE ===== */
 const styles = StyleSheet.create({
   container: { flex: 1, padding: 16, backgroundColor: '#fff' },
   header: {
     flexDirection: 'row',
     justifyContent: 'space-between',
     marginBottom: 12,
   },
   title: { fontSize: 22, fontWeight: 'bold' },
 
   filterRow: { flexDirection: 'row', marginBottom: 12 },
   filterBtn: {
     paddingHorizontal: 12,
     paddingVertical: 6,
     borderRadius: 8,
     backgroundColor: '#eee',
     marginRight: 8,
   },
   filterActive: { backgroundColor: '#000' },
 
   sectionWarning: { color: 'red', fontWeight: 'bold', marginVertical: 8 },
   section: { fontWeight: 'bold', marginVertical: 8 },
 
   item: {
     flexDirection: 'row',
     padding: 12,
     borderRadius: 10,
     backgroundColor: '#fafafa',
     marginBottom: 8,
     alignItems: 'center',
   },
   image: {
     width: 44,
     height: 44,
     borderRadius: 6,
     borderWidth: 1,
     borderStyle: 'dashed',
     marginRight: 12,
   },
   name: { fontWeight: 'bold' },
   sub: { color: 'gray', fontSize: 12 },
 });
 