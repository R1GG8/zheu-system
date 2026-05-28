<template>
  <div class="app-container">
    <!-- Sidebar -->
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
        </nav>
      </div>

      <div style="border-top: 1px solid var(--border-color); padding-top: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
          <div style="width: 36px; height: 36px; border-radius: 50%; background: var(--bg-card); display: flex; align-items: center; justify-content: center;">👤</div>
          <div>
            <div style="font-size: 0.85rem; font-weight: 600;">{{ auth.user?.full_name }}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">{{ auth.user?.username }}</div>
          </div>
        </div>
        <button @click="handleLogout" class="btn" style="width: 100%; background-color: #ef444415; color: #ef4444;">Выйти</button>
      </div>
    </aside>

    <!-- Content Area -->
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
import { computed } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();

const roleDisplay = computed(() => {
  const roles = { 'RESIDENT': 'Жителя', 'MASTER': 'Мастера', 'ADMIN': 'Диспетчера' };
  return roles[auth.role] || 'Пользователя';
});

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};
</script>