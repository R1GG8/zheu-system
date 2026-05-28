<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
      <h1 style="margin: 0;">Заявки жителей</h1>
      <router-link v-if="auth.role === 'RESIDENT'" to="/create" class="btn btn-primary">+ Новая заявка</router-link>
    </div>

    <div class="table-container">
      <div class="table-header">
        <h3 style="margin: 0;">Обращения</h3>
      </div>
      
      <table>
        <thead>
          <tr>
            <th>Заявка</th>
            <th>Услуга</th>
            <th>Статус</th>
            <th>Дата</th>
            <th style="text-align: right;">Действие</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <!-- Добавили data-label для мобильной верстки -->
            <td data-label="Заявка">
              <div style="font-weight: 700; color: var(--primary);">{{ app.number }}</div>
              <div style="font-size: 0.85rem; font-weight: 500; margin-top: 4px;">{{ app.title }}</div>
            </td>
            <td data-label="Услуга">
              <span style="background: var(--bg-card); padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; border: 1px solid var(--border-color);">
                {{ app.service_type_display }}
              </span>
            </td>
            <td data-label="Статус">
              <span :class="statusClass(app.status)" class="badge">{{ app.status_display }}</span>
            </td>
            <td data-label="Дата" style="color: var(--text-muted); font-size: 0.85rem;">
              {{ new Date(app.created_at).toLocaleDateString() }}
            </td>
            <td style="text-align: right;">
              <button @click="openDetails(app)" class="btn" style="padding: 8px 16px; background-color: rgba(99, 102, 241, 0.1); color: #a5b4fc; font-size: 0.8rem;">Просмотр</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно деталей заявки -->
    <div v-if="selectedApp" class="modal-overlay" @click.self="selectedApp = null">
      <div class="modal-content">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px;">
          <div>
            <span style="font-size: 0.8rem; color: var(--primary); font-weight: 700;">{{ selectedApp.number }}</span>
            <h2 style="margin: 4px 0 0 0;">{{ selectedApp.title }}</h2>
          </div>
          <button @click="selectedApp = null" class="btn" style="background: transparent; color: var(--text-muted); font-size: 1.2rem; padding: 0;">✕</button>
        </div>

        <div style="margin-bottom: 32px;">
          <h4 style="margin-bottom: 12px; color: var(--text-muted);">Описание</h4>
          <p style="background: var(--bg-sidebar); border: 1px solid var(--border-color); padding: 20px; border-radius: var(--radius-md); margin: 0; font-size: 0.95rem; line-height: 1.6;">
            {{ selectedApp.description }}
          </p>
        </div>

        <div v-if="selectedApp.attachments && selectedApp.attachments.length" style="margin-bottom: 32px;">
          <h4 style="margin-bottom: 12px; color: var(--text-muted);">Прикрепленные фото</h4>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <img v-for="att in selectedApp.attachments" :key="att.id" :src="att.file" style="width: 100%; border-radius: var(--radius-md); border: 1px solid var(--border-color);" />
          </div>
        </div>

        <!-- Кнопки управления для диспетчера / мастера -->
        <div v-if="auth.role === 'ADMIN' || auth.role === 'MASTER'" style="margin-bottom: 32px; padding: 20px; background: var(--bg-sidebar); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <h4 style="margin: 0 0 16px 0; color: var(--text-muted);">Управление заявкой</h4>
          
          <!-- Диспетчер: Назначить мастера -->
          <div v-if="auth.role === 'ADMIN'" style="display: flex; gap: 12px; align-items: center;">
            <select v-model="assignmentMasterId" class="form-input" style="flex: 1;">
              <option value="">-- Выберите мастера --</option>
              <option v-for="m in masters" :key="m.id" :value="m.id">{{ m.full_name }}</option>
            </select>
            <button @click="assignMaster" class="btn btn-primary">Назначить</button>
          </div>

          <!-- Мастер: Изменить статус -->
          <div v-if="auth.role === 'MASTER'" style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; gap: 12px;">
              <button @click="changeStatus('IN_PROGRESS')" class="btn" style="background: rgba(245, 158, 11, 0.1); color: #fde047; flex: 1;">В работу</button>
              <button @click="changeStatus('DONE')" class="btn" style="background: rgba(16, 185, 129, 0.1); color: #6ee7b7; flex: 1;">Выполнено</button>
            </div>
            <input v-model="statusChangeComment" type="text" class="form-input" placeholder="Добавить комментарий к изменению статуса" />
          </div>
        </div>

        <!-- История статусов -->
        <div>
          <h4 style="margin-bottom: 16px; color: var(--text-muted);">История изменений</h4>
          <div style="border-left: 2px solid var(--border-color); margin-left: 8px; padding-left: 20px; display: flex; flex-direction: column; gap: 24px;">
            <div v-for="h in selectedApp.status_history" :key="h.id" style="position: relative;">
              <div style="position: absolute; left: -27px; top: 4px; width: 12px; height: 12px; border-radius: 50%; background: var(--primary); border: 2px solid var(--bg-main);"></div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">{{ new Date(h.changed_at).toLocaleString() }}</div>
              <div style="font-weight: 700; font-size: 0.9rem; margin-top: 4px;">{{ h.to_status }}</div>
              <div v-if="h.comment" style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">{{ h.comment }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const applications = ref([]);
const selectedApp = ref(null);
const assignmentMasterId = ref('');
const statusChangeComment = ref('');
const masters = ref([]);

const statusClass = (status) => {
  const classes = {
    'NEW': 'badge-new',
    'IN_PROGRESS': 'badge-progress',
    'DONE': 'badge-done',
    'CANCELED': 'badge-danger'
  };
  return classes[status] || 'badge-new';
};

const openDetails = (app) => {
  selectedApp.value = app;
  assignmentMasterId.value = app.master || '';
};

const assignMaster = async () => {
  if (!assignmentMasterId.value) return;
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/assign_master/`,
      { master_id: assignmentMasterId.value },
      { headers }
    );
    alert('Мастер успешно назначен!');
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Ошибка при назначении.');
  }
};

const changeStatus = async (newStatus) => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.patch(
      `http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/`,
      { 
        status: newStatus,
        comment: statusChangeComment.value 
      },
      { headers }
    );
    alert('Статус обновлен!');
    statusChangeComment.value = '';
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Ошибка при смене статуса.');
  }
};

const loadData = async () => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  const res = await axios.get('http://127.0.0.1:8000/api/applications/', { headers });
  applications.value = Array.isArray(res.data) ? res.data : res.data.results;

  if (auth.role === 'ADMIN') {
    // Временный список для диспетчера
    masters.value = [
      { id: '1b8976b9-4f81-4209-8b43-41bbd0058b21', full_name: 'Иванов С.П. (Сантехник)' },
      { id: '2c9876b9-4f81-4209-8b43-41bbd0058b22', full_name: 'Петров А.В. (Электрик)' }
    ];
  }
};

onMounted(loadData);
</script>