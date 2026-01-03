import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Alert,
  Clipboard,
  Share
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function AddMemberScreen({ navigation }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [inviteCode] = useState('ABC123XYZ');
  const [searchResults, setSearchResults] = useState([]);

  // Mock search function
  const handleSearch = (text) => {
    setSearchQuery(text);
    
    // Simulate search results
    if (text.length > 2) {
      setSearchResults([
        { id: 1, username: 'phamvanx', fullName: 'Phạm Văn X' }
      ]);
    } else {
      setSearchResults([]);
    }
  };

  const handleAddMember = (member) => {
    Alert.alert(
      'Xác nhận',
      `Thêm ${member.fullName} vào nhóm?`,
      [
        { text: 'Hủy', style: 'cancel' },
        {
          text: 'Thêm',
          onPress: () => {
            Alert.alert('Thành công', `Đã thêm ${member.fullName} vào nhóm`);
            setSearchQuery('');
            setSearchResults([]);
          }
        }
      ]
    );
  };

  const copyInviteCode = async () => {
    await Clipboard.setString(inviteCode);
    Alert.alert('Đã copy', 'Mã mời đã được sao chép');
  };

  const shareInviteCode = async () => {
    try {
      await Share.share({
        message: `Tham gia nhóm "Gia đình Nguyễn" với mã: ${inviteCode}`,
      });
    } catch (error) {
      console.error(error);
    }
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
        <Text style={styles.headerTitle}>Thêm thành viên</Text>
        <View style={styles.headerRight} />
      </View>

      <ScrollView style={styles.scrollView}>
        <View style={styles.content}>
          {/* Search Box */}
          <View style={styles.searchContainer}>
            <Ionicons name="search" size={20} color="#999" style={styles.searchIcon} />
            <TextInput
              style={styles.searchInput}
              value={searchQuery}
              onChangeText={handleSearch}
              placeholder="Tìm email / username..."
              placeholderTextColor="#999"
            />
          </View>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <View style={styles.resultsSection}>
              <Text style={styles.sectionTitle}>Kết quả:</Text>
              {searchResults.map((member) => (
                <View key={member.id} style={styles.resultItem}>
                  {/* Avatar */}
                  <View style={styles.avatar}>
                    <Ionicons name="person" size={24} color="#999" />
                  </View>

                  {/* Member Info */}
                  <View style={styles.memberInfo}>
                    <Text style={styles.username}>{member.username}</Text>
                    <Text style={styles.fullName}>{member.fullName}</Text>
                  </View>

                  {/* Add Button */}
                  <TouchableOpacity 
                    style={styles.addButton}
                    onPress={() => handleAddMember(member)}
                  >
                    <Text style={styles.addButtonText}>Thêm</Text>
                  </TouchableOpacity>
                </View>
              ))}
            </View>
          )}

          {/* Invite Code Section */}
          <View style={styles.inviteSection}>
            <Text style={styles.sectionTitle}>Hoặc chia sẻ mã</Text>
            
            <View style={styles.inviteCard}>
              <Text style={styles.inviteCode}>{inviteCode}</Text>
              
              <View style={styles.inviteActions}>
                <TouchableOpacity 
                  style={styles.inviteActionButton}
                  onPress={copyInviteCode}
                >
                  <Text style={styles.inviteActionText}>Sao chép</Text>
                </TouchableOpacity>

                <TouchableOpacity 
                  style={styles.inviteActionButton}
                  onPress={shareInviteCode}
                >
                  <Text style={styles.inviteActionText}>Chia sẻ</Text>
                </TouchableOpacity>
              </View>
            </View>
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
  headerRight: {
    width: 40,
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 16,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#d1d1d6',
    paddingHorizontal: 12,
    marginBottom: 20,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 14,
    fontSize: 15,
    color: '#000',
  },
  resultsSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 12,
  },
  resultItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
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
  username: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    marginBottom: 2,
  },
  fullName: {
    fontSize: 14,
    color: '#666',
  },
  addButton: {
    backgroundColor: '#1c1c1e',
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 6,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  inviteSection: {
    marginTop: 24,
  },
  inviteCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 24,
    alignItems: 'center',
  },
  inviteCode: {
    fontSize: 32,
    fontWeight: '700',
    color: '#000',
    letterSpacing: 3,
    marginBottom: 20,
  },
  inviteActions: {
    flexDirection: 'row',
    gap: 12,
  },
  inviteActionButton: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 24,
    paddingVertical: 10,
    borderRadius: 8,
  },
  inviteActionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#000',
  },
});