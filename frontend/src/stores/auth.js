import { defineStore } from 'pinia';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || 'RESIDENT',
  },
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/token/', { username, password });
        this.token = response.data.access;
        localStorage.setItem('token', this.token);
        
        const decoded = jwtDecode(this.token);
        this.user = {
          id: decoded.user_id,
          username: decoded.username,
          role: decoded.role || 'RESIDENT',
          full_name: decoded.full_name || username
        };
        localStorage.setItem('user', JSON.stringify(this.user));
        
        // Внутри действия login, сразу после успешного получения токена:
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;

        // Имитируем получение FCM токена от браузера/телефона
        const mockFcmToken = "fcm_token_2026_debian_device_12345"; 

        try {
        await axios.post('http://127.0.0.1:8000/api/notifications/device-tokens/', {
            fcm_token: mockFcmToken,
            device_type: 'WEB'
        });
        
        console.log("Устройство зарегистрировано в Firebase на бэкенде!");
        } catch (e) {
        console.log("Не удалось привязать устройство к пушам.");
        }
        return true;
      } catch (error) {
        return false;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common['Authorization'];
    }
  }
});