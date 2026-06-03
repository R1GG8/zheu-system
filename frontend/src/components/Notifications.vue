<template>
  <div style="max-width: 600px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
      <h1 style="margin: 0;">Уведомления</h1>
      <button v-if="hasUnread" @click="markAllAsRead" class="btn" style="background: rgba(99, 102, 241, 0.1); color: #a5b4fc; font-size: 0.8rem;">
        Пометить все как прочитанные
      </button>
    </div>

    <div v-if="list.length" style="display: flex; flex-direction: column; gap: 16px;">
      <div v-for="item in list" :key="item.id" class="card" :style="cardStyle(item.is_read)" style="padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <h3 style="margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
            <!-- Красная точка для непрочитанных -->
            <span v-if="!item.is_read" style="width: 8px; height: 8px; border-radius: 50%; background-color: var(--danger); display: inline-block;"></span>
            {{ item.title }}
          </h3>
          <span style="font-size: 0.75rem; color: var(--text-muted);">
            {{ new Date(item.created_at).toLocaleString() }}
          </span>
        </div>
        <p style="margin: 0; font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; white-space: pre-wrap;">
          {{ item.body }}
        </p>
      </div>
    </div>

    <div v-else class="card" style="text-align: center; padding: 60px;">
      <p style="color: var(--text-muted); margin: 0;">У вас пока нет уведомлений.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const list = ref([]);

const hasUnread = computed(() => {
  return list.value.some(item => !item.is_read);
});

const cardStyle = (isRead) => {
  return isRead 
    ? 'border: 1px solid var(--border-color); opacity: 0.7;'
    : 'border: 1px solid var(--primary); background: rgba(99, 102, 241, 0.03);';
};

const markAllAsRead = async () => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.post('http://127.0.0.1:8000/api/notifications/my/mark_all_as_read/', {}, { headers });
    loadNotifications();
  } catch (e) {
    alert('Не удалось обновить статус.');
  }
};

const loadNotifications = async () => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/notifications/my/', { headers });
    list.value = Array.isArray(res.data) ? res.data : (res.data.results || []);
  } catch (e) {
    console.error("Не удалось загрузить уведомления.");
  }
};

onMounted(loadNotifications);
</script>