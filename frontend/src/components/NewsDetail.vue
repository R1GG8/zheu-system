<template>
  <div v-if="item" style="max-width: 700px; margin: 0 auto;">
    <router-link to="/" style="color: var(--primary); text-decoration: none; font-size: 0.9rem; display: inline-block; margin-bottom: 24px;">
      ← Вернуться к списку новостей
    </router-link>

    <div class="card" style="padding: 40px;">
      <div v-if="item.image" style="width: 100%; max-height: 400px; border-radius: var(--radius-md); overflow: hidden; margin-bottom: 32px;">
        <img :src="item.image" style="width: 100%; height: 100%; object-fit: cover;" />
      </div>

      <h1 style="margin-top: 0; margin-bottom: 12px; font-size: 2rem;">{{ item.title }}</h1>
      
      <div style="display: flex; gap: 16px; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 32px; border-bottom: 1px solid var(--border-color); padding-bottom: 16px;">
        <span>Автор: {{ item.author_name }}</span>
        <span>Дата: {{ new Date(item.created_at).toLocaleString() }}</span>
      </div>

      <!-- preserve-text сохраняет переносы строк и структуру из БД -->
      <div class="preserve-text" style="font-size: 1.05rem; color: var(--text-main);">
        {{ item.content }}
      </div>
    </div>
  </div>
  <div v-else style="text-align: center; padding: 40px;">Загрузка новости...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const item = ref(null);

onMounted(async () => {
  const newsId = route.params.id;
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/news/${newsId}/`);
    item.value = res.data;
  } catch (e) {
    alert('Не удалось загрузить новость.');
  }
});
</script>