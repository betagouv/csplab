import type { MaybeRefOrGetter } from 'vue'
import { computed, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CANDIDATURE_ROUTE_NAME } from '../routes'
import { findCandidaturePosition, findEtapeOfCandidature } from '../utils/position'
import { useCandidatures } from './useCandidatures'

export function useCandidatureNavigation(candidatureUuid: MaybeRefOrGetter<string>) {
  const route = useRoute()
  const router = useRouter()
  const { candidatureKanban, filters } = useCandidatures()

  const position = computed(() => findCandidaturePosition(filters.filteredEtapes.value, toValue(candidatureUuid)))
  const etape = computed(() => findEtapeOfCandidature(candidatureKanban.value, toValue(candidatureUuid)))

  function navigateTo(uuid: string): void {
    void router.replace({ name: CANDIDATURE_ROUTE_NAME, params: { ...route.params, candidatureUuid: uuid } })
  }

  function goPrevious(): void {
    if (position.value?.previousUuid)
      navigateTo(position.value.previousUuid)
  }

  function goNext(): void {
    if (position.value?.nextUuid)
      navigateTo(position.value.nextUuid)
  }

  return { position, etape, goPrevious, goNext }
}
