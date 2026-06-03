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

        <!-- Кнопки управления для Жителя (Отмена) -->
        <div v-if="auth.role === 'RESIDENT' && selectedApp.status === 'NEW'" style="margin-bottom: 32px;">
          <button @click="deleteApp" class="btn" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); width: 100%; border: 1px solid rgba(239,68,68,0.2);">
            Отменить и удалить заявку
          </button>
        </div>

        <!-- Кнопки управления для Диспетчера / Мастера -->
        <div v-if="auth.role === 'ADMIN' || auth.role === 'MASTER'" style="margin-bottom: 32px; padding: 20px; background: var(--bg-sidebar); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <h4 style="margin: 0 0 16px 0; color: var(--text-muted);">Управление заявкой</h4>
          
          <!-- Диспетчер: Назначить мастера -->
          <div v-if="auth.role === 'ADMIN'" style="display: flex; gap: 12px; align-items: center; width: 100%;">
            <select v-model="assignmentMasterId" class="form-input" style="flex: 1;">
              <option value="">-- Выберите мастера --</option>
              <option v-for="m in filteredMasters" :key="m.id" :value="m.id">
                {{ m.full_name || m.username }} ({{ m.position }})
              </option>
            </select>
            <button @click="assignMaster" class="btn btn-primary">Назначить</button>
          </div>

          <!-- Мастер: Если заявка новая (NEW) -->
          <div v-if="auth.role === 'MASTER' && selectedApp.status === 'NEW'">
            <!-- Вариант А: Заявка предложена лично ему жителем -->
            <div v-if="selectedApp.master === auth.user.id" style="display: flex; gap: 12px;">
              <button @click="handleMasterDecision('accept')" class="btn" style="background: rgba(16, 185, 129, 0.1); color: #6ee7b7; flex: 1;">
                ✅ Принять заявку
              </button>
              <button @click="handleMasterDecision('reject')" class="btn" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); flex: 1;">
                ❌ Отклонить заявку
              </button>
            </div>
            
            <!-- Вариант Б: Заявка общая без мастера, берем её сами -->
            <div v-else-if="!selectedApp.master">
              <button @click="selfAssign" class="btn btn-primary" style="width: 100%;">Взять заявку в работу</button>
            </div>
          </div>

          <!-- Мастер: Изменить статус (если заявка уже в работе) -->
          <div v-if="auth.role === 'MASTER' && selectedApp.status === 'IN_PROGRESS'" style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display: flex; gap: 12px;">
              <button @click="changeStatus('DONE')" class="btn" style="background: rgba(16, 185, 129, 0.1); color: #6ee7b7; flex: 1;">Завершить работу (Выполнено)</button>
              <button @click="changeStatus('CANCELED')" class="btn" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); flex: 1;">Отклонить заявку</button>
            </div>
            <input v-model="statusChangeComment" type="text" class="form-input" placeholder="Комментарий к изменению статуса" />
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
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const applications = ref([]);
const selectedApp = ref(null);
const assignmentMasterId = ref('');
const statusChangeComment = ref('');
const masters = ref([]);

const handleMasterDecision = async (decision) => {
  const endpoint = decision === 'accept' ? 'accept_application' : 'reject_application';
  const headers = { Authorization: `Bearer ${auth.token}` };
  
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/${endpoint}/`,
      {},
      { headers }
    );
    const msg = decision === 'accept' ? 'Заявка принята в работу!' : 'Вы отклонили заявку. Она возвращена в общую очередь.';
    alert(msg);
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Не удалось обработать решение.');
  }
};

// Фильтрация мастеров на основе типа заявки (с поддержкой базовой роли)
const filteredMasters = computed(() => {
  if (!selectedApp.value) return [];
  const serviceType = selectedApp.value.service_type;
  return masters.value.filter(m => {
    if (!m.position) return true; 
    const pos = m.position.toLowerCase();
    if (pos === 'мастер' || pos === 'master') return true;
    if (serviceType === 'PLUMBER') {
      return pos.includes('сантехник') || pos.includes('plumber');
    }
    if (serviceType === 'ELECTRICIAN') {
      return pos.includes('электрик') || pos.includes('electrician');
    }
    return true;
  });
});

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

const selfAssign = async () => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/self_assign/`,
      {},
      { headers }
    );
    alert('Вы успешно взяли заявку в работу!');
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Не удалось взять заявку в работу.');
  }
};

const changeStatus = async (newStatus) => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/change_status/`,
      { 
        status: newStatus,
        comment: statusChangeComment.value 
      },
      { headers }
    );
    alert('Статус успешно изменен!');
    statusChangeComment.value = '';
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Ошибка при смене статуса.');
  }
};

const deleteApp = async () => {
  if (!confirm('Вы действительно хотите отменить и удалить эту заявку?')) return;
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    await axios.delete(`http://127.0.0.1:8000/api/applications/${selectedApp.value.id}/`, { headers });
    alert('Заявка отменена.');
    selectedApp.value = null;
    loadData();
  } catch (e) {
    alert('Ошибка удаления.');
  }
};

const loadData = async () => {
  const headers = { Authorization: `Bearer ${auth.token}` };
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/applications/', { headers });
    applications.value = Array.isArray(res.data) ? res.data : res.data.results;
  } catch (e) {
    console.error("Ошибка загрузки заявок", e);
  }

  if (auth.role === 'ADMIN') {
    try {
      const mastersRes = await axios.get('http://127.0.0.1:8000/api/users/masters/', { headers });
      masters.value = Array.isArray(mastersRes.data) ? mastersRes.data : (mastersRes.data.results || []);
    } catch (e) {
      console.error("Ошибка загрузки списка мастеров", e);
    }
  }
};

onMounted(loadData);
</script>