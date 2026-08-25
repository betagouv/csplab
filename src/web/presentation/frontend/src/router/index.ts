import type { RouteRecordRaw } from 'vue-router'
import { candidaturesRoutes } from '@/features/candidatures/routes'
import { etapesRecrutementRoutes } from '@/features/etapes-recrutement/routes'
import { organismesRoutes } from '@/features/organismes/routes'
import { recrutementsRoutes } from '@/features/recrutements/routes'

const appRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
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
  ...organismesRoutes,
  notFoundRoute,
]
