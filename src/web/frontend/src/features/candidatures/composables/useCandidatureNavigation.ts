import type { MaybeRefOrGetter } from 'vue'
import { computed, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CANDIDATURE_ROUTE_NAME } from '../routes'
import { findEtapeOfCandidature, findPositionInList } from '../utils/position'
import { useCandidatures } from './useCandidatures'
import { useCandidaturesView } from './useCandidaturesView'

export function useCandidatureNavigation(candidatureUuid: MaybeRefOrGetter<string>) {
  const route = useRoute()
  const router = useRouter()
  const { candidatureKanban, filters } = useCandidatures()

  const vue = useCandidaturesView()

  const sequence = computed(() => vue.value === 'liste'
    ? filters.filteredCandidatures.value
    : filters.filteredEtapes.value.flatMap(etape => etape.candidatures),
  )

  const position = computed(() => findPositionInList(sequence.value, toValue(candidatureUuid)))
  const etape = computed(() => findEtapeOfCandidature(candidatureKanban.value, toValue(candidatureUuid)))

  function navigateTo(uuid: string): void {
    const navigate = route.params.candidatureUuid ? router.replace : router.push
    void navigate({
      name: CANDIDATURE_ROUTE_NAME,
      params: { ...route.params, candidatureUuid: uuid },
      query: route.query,
    })
  }

  function goPrevious(): void {
    if (position.value?.previousUuid)
      navigateTo(position.value.previousUuid)
  }

  function goNext(): void {
    if (position.value?.nextUuid)
      navigateTo(position.value.nextUuid)
  }

  return { position, etape, navigateTo, goPrevious, goNext }
}
