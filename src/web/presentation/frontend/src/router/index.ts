import type { RouteRecordRaw } from 'vue-router'
import { candidaturesRoutes } from '@/features/candidatures/routes'
import { etapesRecrutementRoutes } from '@/features/etapes-recrutement/routes'
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

const notFoundRoute: RouteRecordRaw = {
  path: '/:pathMatch(.*)*',
  name: 'not-found',
  component: () => import('@/views/NotFoundView.vue'),
}

export const routes: RouteRecordRaw[] = [
  ...appRoutes,
  ...recrutementsRoutes,
  ...candidaturesRoutes,
  ...etapesRecrutementRoutes,
  notFoundRoute,
]
