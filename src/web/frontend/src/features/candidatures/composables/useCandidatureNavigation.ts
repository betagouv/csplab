import type { InjectionKey, MaybeRefOrGetter } from 'vue'
import { computed, inject, provide, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CANDIDATURE_ROUTE_NAME } from '../routes'
import { findCandidaturePosition } from '../utils/position'

type CandidatureSequence = (candidatureUuid: string) => string[]

const KEY: InjectionKey<CandidatureSequence> = Symbol('candidature-sequence')

export function provideCandidatureSequence(sequenceOf: CandidatureSequence): void {
  provide(KEY, sequenceOf)
}

export function useCandidatureNavigation(candidatureUuid: MaybeRefOrGetter<string>) {
  const route = useRoute()
  const router = useRouter()
  const sequenceOf = inject(KEY)
  if (!sequenceOf) {
    throw new Error('useCandidatureNavigation must be used within provideCandidatureSequence')
  }

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
