import type { CandidaturesViewName } from '@/router/names'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { CANDIDATURE_PANEL_ROUTE_NAMES, CANDIDATURES_VIEW_ROUTE_NAMES } from '@/router/names'

export function useCandidaturePanelRoutes() {
  const route = useRoute()
  const view = computed<CandidaturesViewName>(() => route.meta.candidaturesView ?? 'kanban')

  return {
    view,
    names: computed(() => CANDIDATURE_PANEL_ROUTE_NAMES[view.value]),
    parentName: computed(() => CANDIDATURES_VIEW_ROUTE_NAMES[view.value]),
  }
}
