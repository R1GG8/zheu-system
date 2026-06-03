import { createRouter, createWebHistory } from 'vue-router'
import NewsList from '../components/NewsList.vue'
import NewsDetail from '../components/NewsDetail.vue'
import CreateNews from '../components/CreateNews.vue' // <-- ВЕРНУЛИ ИМПОРТ
import Login from '../components/Login.vue'
import Applications from '../components/Applications.vue'
import CreateApplication from '../components/CreateApplication.vue'
import Profile from '../components/Profile.vue'
import Notifications from '../components/Notifications.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: NewsList },
    { path: '/news/:id', component: NewsDetail },
    { path: '/create-news', component: CreateNews },
    { path: '/login', component: Login },
    { path: '/applications', component: Applications },
    { path: '/create', component: CreateApplication },
    { path: '/profile', component: Profile },
    { path: '/notifications', component: Notifications },
  ]
})

export default router