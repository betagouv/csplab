import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

const router = createRouter({
  history: createWebHistory('/ats/'),
  routes: [{ path: '/', name: 'home', component: () => import('@/features/ats/HomeView.vue') }],
})

createApp(App).use(router).mount('#ats-app')
