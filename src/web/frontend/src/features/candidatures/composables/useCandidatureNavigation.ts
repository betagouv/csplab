import type { InjectionKey, MaybeRefOrGetter } from 'vue'
import { computed, inject, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CANDIDATURE_ROUTE_NAME } from '../routes'
import { findCandidaturePosition } from '../utils/position'

export const CANDIDATURE_SEQUENCE: InjectionKey<(candidatureUuid: string) => string[]> = Symbol('candidature-sequence')

export function useCandidatureNavigation(candidatureUuid: MaybeRefOrGetter<string>) {
  const route = useRoute()
  const router = useRouter()
  const sequenceOf = inject(CANDIDATURE_SEQUENCE, () => [])

  const position = computed(() => findCandidaturePosition(sequenceOf(toValue(candidatureUuid)), toValue(candidatureUuid)))

  function navigateTo(uuid: string): void {
    const navigate = route.params.candidatureUuid ? router.replace : router.push
    void navigate({ name: CANDIDATURE_ROUTE_NAME, params: { ...route.params, candidatureUuid: uuid } })
  }

  function goPrevious(): void {
    if (position.value?.previousUuid) {
      navigateTo(position.value.previousUuid)
    }
  }

  function goNext(): void {
    if (position.value?.nextUuid) {
      navigateTo(position.value.nextUuid)
    }
  }

  return { position, navigateTo, goPrevious, goNext }
}
