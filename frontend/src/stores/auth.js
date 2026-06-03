import { defineStore } from 'pinia';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { requestNotificationPermission } from '../services/firebase';

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

        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;

        const realFcmToken = await requestNotificationPermission(); 

        if (realFcmToken) {
          try {
            await axios.post('http://127.0.0.1:8000/api/notifications/device-tokens/', {
              fcm_token: realFcmToken,
              device_type: 'WEB'
            });
            console.log("Реальное устройство успешно привязано к пушам!");
          } catch (e) {
            console.log("Не удалось сохранить токен устройства на сервере.");
          } 
        }
        
        return true; 

      } catch (error) { 
        console.error("Ошибка входа:", error);
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