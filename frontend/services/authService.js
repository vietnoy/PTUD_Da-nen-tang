import api from './api';
import storage from './storage';

const authService = {
  register: (payload) => {
  try{
    return apiClient.post('/register', {
    email: payload.email,
    password: payload.password,
    name: payload.name,
    language: payload.language,
    timezone: payload.timezone,
    deviceId: payload.deviceId,
    user_name: payload.user_name,
  });
  } catch (error){
    console.error('Register service error:', error);
    throw error;
  };
  },
  login: async (email, password) => {
    try {
      // Gọi API login
      const response = await api.post('/auth/login', {
        email: email,
        password: password,
      });

      // Lấy data từ response
      const data = response.data;

      // Lưu token vào AsyncStorage
      if (data.token) {
        await storage.saveToken(data.token);
        console.log('Token saved successfully');
      }

      // Lưu thông tin user vào AsyncStorage
      if (data.user) {
        await storage.saveUser(data.user);
        console.log('User info saved successfully');
      }

      // Trả về toàn bộ data
      return data;
    } catch (error) {
      // Ném lỗi để component xử lý
      console.error('Login service error:', error);
      throw error;
    }
  },

  /**
   * Kiểm tra đã đăng nhập chưa
   * @returns {Promise<boolean>}
   */
  isAuthenticated: async () => {
    try {
      const token = await storage.getToken();
      return !!token; // Trả về true nếu có token, false nếu không
    } catch (error) {
      return false;
    }
  },

  /**
   * Đăng xuất
   */
  logout: async () => {
    try {
      // Xóa toàn bộ dữ liệu
      await storage.clearAll();
      console.log('Logged out successfully');
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  },

  /**
   * Lấy thông tin user hiện tại
   */
  getCurrentUser: async () => {
    try {
      const user = await storage.getUser();
      return user;
    } catch (error) {
      console.error('Get current user error:', error);
      return null;
    }
  },
};

export default authService;