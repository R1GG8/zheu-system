<template>
  <div style="display: flex; justify-content: center; padding-top: 60px;">
    <div class="card" style="width: 100%; max-width: 420px;">
      <h2 style="text-align: center; margin-top: 0; margin-bottom: 8px;">Авторизация</h2>
      <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 32px;">Войдите в личный кабинет ЖЭУ</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">Логин или Email</label>
          <input v-model="username" type="text" required class="form-input" placeholder="Введите имя или почту" />
        </div>
        
        <div class="form-group" style="margin-bottom: 32px;">
          <label class="form-label">Пароль</label>
          <input v-model="password" type="password" required class="form-input" placeholder="••••••••" />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">Войти</button>
      </form>
      
      <div v-if="error" style="margin-top: 20px; padding: 12px; background: rgba(239, 68, 68, 0.1); color: var(--danger); border-radius: var(--radius-md); text-align: center; font-size: 0.85rem;">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  const success = await auth.login(username.value, password.value);
  if (success) {
    router.push('/applications');
  } else {
    error.value = 'Ошибка входа. Проверьте данные.';
  }
};
</script>