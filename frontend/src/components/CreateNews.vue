<template>
  <div style="max-width: 540px; margin: 0 auto;">
    <h1 style="margin-bottom: 8px;">Опубликовать новость</h1>
    <p style="color: var(--text-muted); margin-bottom: 32px;">Новость увидят все жители в своей ленте событий</p>

    <div class="card">
      <form @submit.prevent="submitNews">
        <div class="form-group">
          <label class="form-label">Заголовок новости</label>
          <input v-model="form.title" type="text" required class="form-input" placeholder="Например: Отключение горячей воды 26 мая" />
        </div>

        <div class="form-group">
          <label class="form-label">Содержание</label>
          <textarea v-model="form.content" required class="form-input" style="min-height: 150px; font-family: inherit;" placeholder="Укажите подробности для жителей..."></textarea>
        </div>

        <div class="form-group" style="margin-bottom: 32px;">
          <label class="form-label">Изображение (по желанию)</label>
          <input type="file" @change="handleFile" class="form-input" />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">Опубликовать</button>
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
const file = ref(null);

const form = reactive({
  title: '',
  content: ''
});

const handleFile = (e) => {
  file.value = e.target.files[0];
};

const submitNews = async () => {
  const formData = new FormData();
  formData.append('title', form.title);
  formData.append('content', form.content);
  if (file.value) {
    formData.append('image', file.value);
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/news/', formData, {
      headers: { 
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    router.push('/');
  } catch (e) {
    alert('Не удалось опубликовать. У вас есть права администратора?');
  }
};
</script>