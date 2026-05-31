<template>
  <div>
    <!-- Шапка новостей с кнопкой для Администратора -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; gap: 16px;">
      <h1 style="margin: 0; font-size: 1.8rem;">События и Объявления дома</h1>
      <router-link v-if="auth.role === 'ADMIN'" to="/create-news" class="btn btn-primary">+ Написать новость</router-link>
    </div>
    
    <div v-if="news.length" class="grid-container">
      <article v-for="item in news" :key="item.id" class="card" style="display: flex; flex-direction: column; padding: 0; overflow: hidden;">
        <div style="height: 180px; background-color: var(--bg-sidebar); display: flex; align-items: center; justify-content: center; overflow: hidden;">
          <img v-if="item.image" :src="item.image" style="width: 100%; height: 100%; object-fit: cover;" />
          <span v-else style="color: var(--text-muted);">Нет фото</span>
        </div>
        <div style="padding: 24px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <h3 style="margin: 0 0 12px 0; font-size: 1.2rem;">{{ item.title }}</h3>
            <!-- Выводим только первые 150 символов -->
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px; line-height: 1.5;">
              {{ truncateText(item.content) }}
            </p>
          </div>
          
          <div style="display: flex; flex-direction: column; gap: 12px;">
            <!-- Сетка для кнопок (Читать и Удалить) -->
            <div style="display: flex; gap: 12px;">
              <router-link :to="`/news/${item.id}`" class="btn" style="background: rgba(99, 102, 241, 0.1); color: #a5b4fc; flex: 1; padding: 8px 0; font-size: 0.8rem; text-align: center;">
                Читать далее →
              </router-link>
              
              <!-- Кнопка удаления (видна только ADMIN) -->
              <button v-if="auth.role === 'ADMIN'" @click="deleteNews(item.id)" class="btn" style="background: rgba(239, 68, 68, 0.1); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); padding: 8px 12px; font-size: 0.8rem;">
                🗑️
              </button>
            </div>
            
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); border-top: 1px solid var(--border-color); padding-top: 16px;">
              <span>{{ item.author_name || 'Администрация' }}</span>
              <span>{{ new Date(item.created_at).toLocaleDateString() }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>
    
    <div v-else class="card" style="text-align: center; padding: 60px;">
      <p style="color: var(--text-muted); margin: 0;">Объявлений пока нет.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const news = ref([]);

const truncateText = (text) => {
  if (!text) return '';
  return text.length > 150 ? text.substring(0, 150) + '...' : text;
};

// Функция удаления новости
const deleteNews = async (newsId) => {
  if (!confirm('Вы действительно хотите безвозвратно удалить эту новость?')) return;
  const headers = { Authorization: `Bearer ${auth.token}` };
  
  try {
    await axios.delete(`http://127.0.0.1:8000/api/news/${newsId}/`, { headers });
    alert('Новость успешно удалена!');
    loadNews(); // Обновляем список на клиенте [3]
  } catch (e) {
    alert('Не удалось удалить новость. Недостаточно прав.');
  }
};

const loadNews = async () => {
  const res = await axios.get('http://127.0.0.1:8000/api/news/');
  news.value = Array.isArray(res.data) ? res.data : res.data.results;
};

onMounted(loadNews);
</script>