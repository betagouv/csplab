import type { RouteRecordRaw } from 'vue-router'

export const etapesRecrutementRoutes: RouteRecordRaw[] = [
  {
    path: '/mes-recrutements/:recrutementUuid/etapes-recrutement',
    name: 'recrutement-etapes-recrutement',
    component: () => import('./views/OffreEtapesRecrutementView.vue'),
  },
]
