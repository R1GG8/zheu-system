<template>
  <div v-if="profile" style="max-width: 600px; margin: 0 auto;">
    <h1 style="margin-bottom: 32px;">Личный кабинет</h1>

    <div class="card" style="display: flex; flex-direction: column; gap: 24px;">
      <div style="display: flex; align-items: center; gap: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 24px;">
        <div style="width: 64px; height: 64px; border-radius: 50%; background: var(--bg-sidebar); display: flex; align-items: center; justify-content: center; font-size: 1.8rem;">👤</div>
        <div>
          <h2 style="margin: 0;">{{ profile.full_name || profile.username }}</h2>
          <span class="badge" :class="roleClass" style="margin-top: 8px;">{{ roleDisplay }}</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <div class="form-group">
          <label class="form-label">Логин (ID)</label>
          <div class="form-input" style="background-color: var(--bg-sidebar); opacity: 0.8;">{{ profile.username }}</div>
        </div>
        <div class="form-group">
          <label class="form-label">Почта</label>
          <div class="form-input" style="background-color: var(--bg-sidebar); opacity: 0.8;">{{ profile.email }}</div>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Контактный телефон</label>
        <div class="form-input" style="background-color: var(--bg-sidebar); opacity: 0.8;">{{ profile.phone || 'Не указан' }}</div>
      </div>

      <!-- Блок информации для Жителя (Дом и Квартира) -->
      <div v-if="profile.role === 'RESIDENT' && profile.resident_profile" style="background: var(--bg-sidebar); padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
        <h3 style="margin-top: 0; margin-bottom: 16px; color: var(--primary);">Адрес проживания</h3>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div><strong style="color: var(--text-muted);">Дом:</strong> {{ profile.resident_profile.building_address || 'Не закреплен' }}</div>
          <div><strong style="color: var(--text-muted);">Квартира:</strong> №{{ profile.resident_profile.apartment_number || 'Не указана' }}</div>
        </div>
      </div>

      <!-- Блок информации для Мастера/Админа (Должность и Отдел) -->
      <div v-if="profile.role !== 'RESIDENT' && profile.employee_profile" style="background: var(--bg-sidebar); padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
        <h3 style="margin-top: 0; margin-bottom: 16px; color: var(--primary);">Служебная информация</h3>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <div><strong style="color: var(--text-muted);">Должность:</strong> {{ profile.employee_profile.position }}</div>
          <div><strong style="color: var(--text-muted);">Отдел:</strong> {{ profile.employee_profile.department || 'Управляющая компания' }}</div>
          <div><strong style="color: var(--text-muted);">Статус доступности:</strong> {{ profile.employee_profile.is_active_worker ? 'Доступен для выездов' : 'Занят' }}</div>
        </div>
      </div>
    </div>
  </div>
  <div v-else style="text-align: center; padding: 40px;">Загрузка личного кабинета...</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const profile = ref(null);

const roleDisplay = computed(() => {
  const roles = { 'RESIDENT': 'Житель', 'MASTER': 'Мастер', 'ADMIN': 'Диспетчер (Админ)' };
  return roles[profile.value?.role] || 'Пользователь';
});

const roleClass = computed(() => {
  const classes = { 'RESIDENT': 'badge-new', 'MASTER': 'badge-progress', 'ADMIN': 'badge-done' };
  return classes[profile.value?.role] || 'badge-new';
});

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/profile/', {
      headers: { Authorization: `Bearer ${auth.token}` }
    });
    profile.value = res.data;
  } catch (e) {
    alert('Не удалось загрузить данные профиля.');
  }
});
</script>