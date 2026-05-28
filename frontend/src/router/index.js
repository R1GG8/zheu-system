import { createRouter, createWebHistory } from 'vue-router'
import NewsList from '../components/NewsList.vue'
import Login from '../components/Login.vue'
import Applications from '../components/Applications.vue'
import CreateApplication from '../components/CreateApplication.vue'
import CreateNews from '../components/CreateNews.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: NewsList },
    { path: '/login', component: Login },
    { path: '/applications', component: Applications },
    { path: '/create', component: CreateApplication },
    { path: '/create-news', component: CreateNews },
  ]
})

export default router