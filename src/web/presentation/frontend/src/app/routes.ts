import type { RouteRecordRaw } from 'vue-router'

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/features/ats/HomeView.vue'),
  },
  {
    path: '/mes-recrutements',
    name: 'mes-recrutements',
    component: () => import('@/features/ats/recrutements/MesRecrutementsView.vue'),
  },
]
