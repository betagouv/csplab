import type { LocationQueryRaw } from 'vue-router'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export type CandidaturesViewName = 'kanban' | 'liste'

export const CANDIDATURES_VIEW_QUERY_PARAM = 'vue'

const DEFAULT_VIEW: CandidaturesViewName = 'kanban'

export function candidaturesViewOf(query: Record<string, unknown>): CandidaturesViewName {
  return query[CANDIDATURES_VIEW_QUERY_PARAM] === 'liste' ? 'liste' : DEFAULT_VIEW
}

export function candidaturesViewQuery(view: CandidaturesViewName): LocationQueryRaw {
  return view === DEFAULT_VIEW ? {} : { [CANDIDATURES_VIEW_QUERY_PARAM]: view }
}

export function useCandidaturesView() {
  const route = useRoute()
  return computed(() => candidaturesViewOf(route.query))
}
