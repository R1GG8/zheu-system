<!-- Обновленный шаблон App.vue (боковое меню) -->
<template>
  <div class="app-container">
    <aside v-if="auth.isAuthenticated" class="sidebar">
      <div>
        <div class="logo-container">
          <div class="logo-badge">Ж</div>
          <div>
            <h3 style="margin: 0; font-size: 1rem;">ЖЭУ Контроль</h3>
            <span style="font-size: 0.75rem; color: var(--text-muted);">Кабинет {{ roleDisplay }}</span>
          </div>
        </div>

        <nav class="nav-menu">
          <router-link to="/" class="nav-item">📰 События и Новости</router-link>
          <router-link to="/applications" class="nav-item">💼 Диспетчерская</router-link>
          <router-link to="/create" v-if="auth.role === 'RESIDENT'" class="nav-item">✍️ Подать заявку</router-link>
          <router-link to="/profile" class="nav-item">👤 Личный кабинет</router-link>
          
          <router-link to="/notifications" class="nav-item" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <span>🔔 Уведомления</span>
            <span v-if="unreadCount > 0" style="background-color: var(--danger); color: white; font-size: 0.75rem; font-weight: 800; padding: 2px 8px; border-radius: 9999px; line-height: 1;">
              {{ unreadCount }}
            </span>
          </router-link>
        </nav>
      </div>

      <!-- Кнопка темы и Юзер -->
      <div style="border-top: 1px solid var(--border-color); padding-top: 20px; display: flex; flex-direction: column; gap: 16px;">
        <!-- Переключатель тем -->
        <button @click="toggleTheme" class="btn" style="background: rgba(255,255,255,0.05); color: var(--text-main); font-size: 0.85rem;">
          {{ isDark ? '☀️ Светлая тема' : '🌙 Темная тема' }}
        </button>

        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--bg-card); display: flex; align-items: center; justify-content: center;">👤</div>
          <div>
            <div style="font-size: 0.85rem; font-weight: 600;">{{ auth.user?.full_name }}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">{{ auth.user?.username }}</div>
          </div>
        </div>
        <button @click="handleLogout" class="btn" style="width: 100%; background-color: #ef444415; color: #ef4444;">Выйти</button>
      </div>
    </aside>

    <div class="main-content">
      <header v-if="!auth.isAuthenticated" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
        <h2 style="margin: 0;">ЖЭУ Портал 2026</h2>
        <router-link to="/login" class="btn btn-primary">Войти в кабинет</router-link>
      </header>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
// Внутри скрипта App.vue
import { ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const isDark = ref(localStorage.getItem('theme') !== 'light');
const unreadCount = ref(0);

// Загрузка количества непрочитанных уведомлений из базы
const loadUnreadCount = async () => {
  if (auth.isAuthenticated) {
    const headers = { Authorization: `Bearer ${auth.token}` };
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/notifications/my/', { headers });
      const list = Array.isArray(res.data) ? res.data : (res.data.results || []);
      // Считаем только те, у которых is_read === false
      unreadCount.value = list.filter(item => !item.is_read).length;
    } catch (e) {
      console.log("Не удалось загрузить счетчик уведомлений.");
    }
  }
};

// Сбрасываем счетчик, если пользователь зашел на страницу уведомлений
watch(() => route.path, (newPath) => {
  if (newPath === '/notifications') {
    unreadCount.value = 0;
  } else {
    loadUnreadCount();
  }
});

onMounted(() => {
  document.body.className = isDark.value ? 'dark' : 'light-theme';
  loadUnreadCount();
  
  // Каждые 30 секунд проверяем базу на наличие новых уведомлений (простой поллинг)
  setInterval(() => {
    loadUnreadCount();
  }, 30000);
});


const roleDisplay = computed(() => {
  const roles = { 'RESIDENT': 'Жителя', 'MASTER': 'Мастера', 'ADMIN': 'Диспетчера' };
  return roles[auth.role] || 'Пользователя';
});

// Логика смены темы
const toggleTheme = () => {
  isDark.value = !isDark.value;
  const themeClass = isDark.value ? 'dark' : 'light-theme';
  document.body.className = themeClass;
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
};

onMounted(() => {
  // Задаем тему при инициализации
  document.body.className = isDark.value ? 'dark' : 'light-theme';
});

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};
</script>