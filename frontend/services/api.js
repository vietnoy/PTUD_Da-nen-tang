import axios from 'axios';
import storage from './storage';

// TODO: Thay đổi BASE_URL này thành URL backend thực tế của bạn
// Ví dụ: 'http://192.168.1.5:3000/api' (IP máy bạn)
// Hoặc: 'http://localhost:3000/api' (nếu test trên web)
const BASE_URL = 'http://192.168.1.100:3000/api';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Tự động thêm token vào header
api.interceptors.request.use(
  async (config) => {
    const token = await storage.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Xử lý lỗi
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response) {
      // Server trả về response với status code lỗi
      const { status, data } = error.response;
      
      if (status === 401) {
        // Token hết hạn
        await storage.clearAll();
        console.log('Token expired - cleared storage');
      }
      
      // Trả về error message từ backend
      return Promise.reject({
        message: data.message || 'Đã xảy ra lỗi',
        status: status,
        data: data,
      });
    } else if (error.request) {
      // Request được gửi nhưng không nhận được response
      console.error('Network Error:', error.message);
      return Promise.reject({
        message: 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra kết nối mạng.',
      });
    } else {
      // Lỗi khác
      console.error('Error:', error.message);
      return Promise.reject({
        message: 'Đã xảy ra lỗi không xác định',
      });
    }
  }
);

export default api;