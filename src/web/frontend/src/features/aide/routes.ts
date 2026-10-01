import type { RouteRecordRaw } from 'vue-router'

export const aideRoutes: RouteRecordRaw[] = [
  {
    path: '/aide',
    name: 'aide',
    component: () => import('./views/AideView.vue'),
  },
]
