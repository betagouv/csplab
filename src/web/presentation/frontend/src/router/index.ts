import type { RouteRecordRaw } from 'vue-router'
import { recrutementsRoutes } from '@/features/recrutements/routes'

const appRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/parametres',
    name: 'parametres',
    component: () => import('@/views/ParametresView.vue'),
  },
]

export const routes: RouteRecordRaw[] = [...appRoutes, ...recrutementsRoutes]
