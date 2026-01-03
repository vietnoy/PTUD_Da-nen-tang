import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Alert,
  Clipboard
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function GroupDetailScreen({ navigation }) {
  const [inviteCode] = useState('ABC123XYZ');
  const [members] = useState([
    { id: 1, name: 'Nguyễn Văn A', role: 'Owner', avatar: null },
    { id: 2, name: 'Trần Thị B', role: 'Admin', avatar: null },
    { id: 3, name: 'Nguyễn Văn C', role: 'Member', avatar: null },
  ]);

  const copyInviteCode = () => {
    Clipboard.setString(inviteCode);
    Alert.alert('Đã copy', 'Mã mời đã được sao chép vào clipboard');
  };

  const handleAddMember = () => {
    Alert.alert('Thêm thành viên', 'Chức năng thêm thành viên');
  };

  const handleMemberOptions = (member) => {
    Alert.alert(
      member.name,
      'Chọn hành động',
      [
        { text: 'Xem thông tin', onPress: () => {} },
        { text: 'Xóa khỏi nhóm', style: 'destructive', onPress: () => {} },
        { text: 'Hủy', style: 'cancel' }
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
        <Text style={styles.headerTitle}>Gia đình Nguyễn</Text>
        <TouchableOpacity style={styles.menuButton}>
          <Ionicons name="ellipsis-vertical" size={24} color="#000" />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.scrollView}>
        <View style={styles.content}>
          {/* Invite Code Card */}
          <View style={styles.inviteCard}>
            <Text style={styles.inviteLabel}>Mã mời nhóm:</Text>
            <View style={styles.inviteCodeContainer}>
              <Text style={styles.inviteCode}>{inviteCode}</Text>
              <TouchableOpacity 
                onPress={copyInviteCode}
                style={styles.copyButton}
              >
                <Text style={styles.copyButtonText}>COPY</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Members Section */}
          <View style={styles.membersSection}>
            <Text style={styles.sectionTitle}>Thành viên ({members.length})</Text>

            {/* Member List */}
            {members.map((member, index) => (
              <View key={member.id} style={styles.memberItem}>
                {/* Avatar */}
                <View style={styles.avatar}>
                  <Ionicons name="person" size={24} color="#999" />
                </View>

                {/* Member Info */}
                <View style={styles.memberInfo}>
                  <Text style={styles.memberName}>{member.name}</Text>
                  <Text style={styles.memberRole}>{member.role}</Text>
                </View>

                {/* Options Button (only for non-owners or show for all) */}
                {index === 2 && (
                  <TouchableOpacity 
                    style={styles.optionsButton}
                    onPress={() => handleMemberOptions(member)}
                  >
                    <Ionicons name="ellipsis-vertical" size={20} color="#666" />
                  </TouchableOpacity>
                )}
              </View>
            ))}

            {/* Add Member Button */}
            <TouchableOpacity 
              style={styles.addMemberButton}
              onPress={handleAddMember}
              activeOpacity={0.7}
            >
              <Ionicons name="add" size={20} color="#000" />
              <Text style={styles.addMemberText}>Thêm thành viên</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </View>
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
  menuButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 16,
  },
  inviteCard: {
    backgroundColor: '#e8f5e9',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  inviteLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  inviteCodeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  inviteCode: {
    fontSize: 24,
    fontWeight: '700',
    color: '#000',
    letterSpacing: 2,
  },
  copyButton: {
    paddingHorizontal: 16,
    paddingVertical: 6,
  },
  copyButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2e7d32',
  },
  membersSection: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#000',
    marginBottom: 16,
  },
  memberItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#f0f0f0',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
    borderWidth: 2,
    borderStyle: 'dashed',
    borderColor: '#d1d1d6',
  },
  memberInfo: {
    flex: 1,
  },
  memberName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 4,
  },
  memberRole: {
    fontSize: 14,
    color: '#666',
  },
  optionsButton: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addMemberButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    marginTop: 8,
    borderWidth: 1,
    borderColor: '#d1d1d6',
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  addMemberText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginLeft: 8,
  },
});