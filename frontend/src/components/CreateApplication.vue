<template>
  <!-- Исправлено: теперь тут валидный CSS max-width вместо max-w -->
  <div style="max-width: 540px; margin: 0 auto;">
    <h1 style="margin-bottom: 8px;">Новая заявка</h1>
    <p style="color: var(--text-muted); margin-bottom: 32px;">Заполните форму для вызова специалиста</p>

    <div class="card">
      <form @submit.prevent="submitApp">
        <div class="form-group">
          <label class="form-label">Тип проблемы</label>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <button type="button" @click="form.service_type = 'PLUMBER'" :style="catStyle('PLUMBER')" class="btn">🚰 Сантехник</button>
            <button type="button" @click="form.service_type = 'ELECTRICIAN'" :style="catStyle('ELECTRICIAN')" class="btn">⚡ Электрик</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Тема</label>
          <input v-model="form.title" type="text" required class="form-input" placeholder="Например: Протечка трубы на кухне" />
        </div>

        <div class="form-group">
          <label class="form-label">Подробное описание</label>
          <textarea v-model="form.description" required class="form-input" style="min-height: 120px; font-family: inherit;" placeholder="Укажите детали..."></textarea>
        </div>

        <div class="form-group" style="margin-bottom: 32px;">
          <label class="form-label">Прикрепить фото (по желанию)</label>
          <div style="border: 2px dashed var(--border-color); border-radius: var(--radius-md); padding: 24px; text-align: center; cursor: pointer; position: relative;">
            <input type="file" @change="handleFile" multiple style="position: absolute; inset: 0; opacity: 0; cursor: pointer;" />
            <div style="font-size: 1.5rem; margin-bottom: 8px;">📸</div>
            <span style="font-size: 0.85rem; color: var(--text-muted);">{{ fileLabel }}</span>
          </div>
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">Отправить</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();
const files = ref([]);
const fileLabel = ref('Выберите файлы или перетащите их сюда');

const form = reactive({
  title: '',
  description: '',
  service_type: 'PLUMBER'
});

const catStyle = (type) => {
  return form.service_type === type
    ? 'background-color: rgba(99, 102, 241, 0.1); border: 2px solid var(--primary); color: white;'
    : 'background-color: var(--bg-sidebar); border: 2px solid var(--border-color); color: var(--text-muted);';
};

const handleFile = (e) => {
  files.value = Array.from(e.target.files);
  fileLabel.value = `Выбрано файлов: ${files.value.length}`;
};

const submitApp = async () => {
  const formData = new FormData();
  formData.append('title', form.title);
  formData.append('description', form.description);
  formData.append('service_type', form.service_type);
  files.value.forEach(file => {
    formData.append('uploaded_images', file);
  });

  try {
    await axios.post('http://127.0.0.1:8000/api/applications/', formData, {
      headers: { 
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    router.push('/applications');
  } catch (e) {
    alert('Ошибка отправки');
  }
};
</script>