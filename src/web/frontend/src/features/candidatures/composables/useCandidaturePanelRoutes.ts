import type { CandidaturesLayoutName } from '@/router/names'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { CANDIDATURE_PANEL_ROUTE_NAMES, CANDIDATURES_LAYOUT_ROUTE_NAMES } from '@/router/names'

export function useCandidaturePanelRoutes() {
  const route = useRoute()
  const layout = computed<CandidaturesLayoutName>(() => route.meta.candidaturesLayout ?? 'kanban')

  return {
    layout,
    names: computed(() => CANDIDATURE_PANEL_ROUTE_NAMES[layout.value]),
    parentName: computed(() => CANDIDATURES_LAYOUT_ROUTE_NAMES[layout.value]),
  }
}
