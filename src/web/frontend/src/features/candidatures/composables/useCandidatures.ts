import type { CandidatureListe, EtapeRecrutementDetailedCandidatures, MotifRefus, PaginatedCandidatureListeList } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { defineQuery, useQuery, useQueryCache } from '@pinia/colada'
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from '@/composables/ui/useToast'
import { peekRecrutementIntitule, recrutementDetailQuery } from '@/features/recrutements/queries'
import { patchEtapeCandidatures } from '../api'
import { candidaturesQuery } from '../queries'
import { useCandidaturesFilters } from './useCandidaturesFilters'

export interface MoveCandidatureParams {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
  motifRefus?: MotifRefus
}

export interface MoveCandidaturesBatchParams {
  candidaturesByEtape: Map<string, string[]>
  targetColumnId: string
  motifRefus?: MotifRefus
}

export const useCandidatures = defineQuery(() => {
  const route = useRoute()
  const recrutementUuid = computed<string | null>(() => {
    const param = route.params.recrutementUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const organismeUuid = computed<string | null>(() => {
    const param = route.params.organismeUuid
    return typeof param === 'string' && param !== '' ? param : null
  })

  const queryCache = useQueryCache()

  const detail = useQuery(() => ({
    ...recrutementDetailQuery({
      organismeUuid: organismeUuid.value ?? '',
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: (
      recrutementUuid.value !== null
      && organismeUuid.value !== null
    ),
  }))

  const candidaturesResponse = useQuery(() => ({
    ...candidaturesQuery({
      organismeUuid: organismeUuid.value ?? '',
      recrutementUuid: recrutementUuid.value ?? '',
    }),
    enabled: (
      recrutementUuid.value !== null
      && organismeUuid.value !== null
    ),
  }))

  const recrutementDetail = computed<RecrutementDetail | null>(
    () => detail.data.value ?? null,
  )
  const candidatures = computed<CandidatureListe[]>(() => candidaturesResponse.data.value?.results ?? [])

  const intitule = computed<string | null>(() => {
    if (recrutementDetail.value?.intitule) {
      return recrutementDetail.value.intitule
    }
    if (!organismeUuid.value || !recrutementUuid.value) {
      return null
    }
    return peekRecrutementIntitule(queryCache, organismeUuid.value, recrutementUuid.value)
  })

  const recrutementEtapes = computed(() => detail.data.value?.etapes ?? [])
  const candidatureKanban = computed<EtapeRecrutementDetailedCandidatures[]>(() =>
    recrutementEtapes.value.map(etape => ({
      ...etape,
      candidatures: candidatures.value.filter(c => c.etape.etape_uuid === etape.etape_uuid),
    })),
  )

  const pendingDetail = computed(() => detail.isPending.value)
  const pendingCandidatures = computed(() => candidaturesResponse.isPending.value)

  const error = computed<unknown>(() =>
    detail.error.value ?? candidaturesResponse.error.value,
  )

  function findCandidature(uuid: string): CandidatureListe | null {
    return candidatures.value.find(c => c.uuid === uuid) ?? null
  }

  const totalCount = computed(() => candidatures.value.length)

  const { addToast } = useToast()

  function candidaturesKey() {
    return candidaturesQuery({
      organismeUuid: organismeUuid.value!,
      recrutementUuid: recrutementUuid.value!,
    }).key
  }

  function assignEtape(uuids: Set<string>, etape: CandidatureListe['etape']): void {
    const previous = candidaturesResponse.data.value
    if (!previous)
      return
    queryCache.setQueryData(candidaturesKey(), {
      ...previous,
      results: previous.results.map(c => uuids.has(c.uuid) ? { ...c, etape } : c),
    })
  }

  async function persistEtapeChange(
    targetColumnId: string,
    candidatureUuids: string[],
    previousData: PaginatedCandidatureListeList,
    motifRefus?: MotifRefus,
  ): Promise<boolean> {
    const key = candidaturesKey()
    try {
      const resultat = await patchEtapeCandidatures(organismeUuid.value!, recrutementUuid.value!, {
        etapeCibleUuid: targetColumnId,
        candidatureUuids,
        motifRefus,
      })
      if (resultat.echecs.length > 0) {
        await queryCache.invalidateQueries({ key })
        addToast({
          variant: 'warning',
          title: 'Certaines candidatures n\'ont pas changé d\'étape',
        })
      }
      return resultat.echecs.length === 0
    }
    catch {
      queryCache.setQueryData(key, previousData)
      addToast({
        variant: 'error',
        title: 'Le changement d\'étape a échoué',
        description: 'Vos candidatures sont restées à leur étape actuelle.',
      })
      return false
    }
  }

  async function moveCandidature(params: MoveCandidatureParams): Promise<boolean> {
    const { sourceColumnId, targetColumnId, cardId, motifRefus } = params

    if (sourceColumnId === targetColumnId)
      return false

    const previous = candidaturesResponse.data.value
    const etape = recrutementEtapes.value.find(e => e.etape_uuid === targetColumnId)
    const candidature = candidatures.value.find(c => c.uuid === cardId)

    if (!previous || !etape || !candidature || candidature.etape.etape_uuid !== sourceColumnId)
      return false

    assignEtape(new Set([cardId]), etape)
    return persistEtapeChange(targetColumnId, [cardId], previous, motifRefus)
  }

  function moveCandidaturesBatch(params: MoveCandidaturesBatchParams): void {
    const { candidaturesByEtape, targetColumnId, motifRefus } = params

    const previous = candidaturesResponse.data.value
    const etape = recrutementEtapes.value.find(e => e.etape_uuid === targetColumnId)
    if (!previous || !etape)
      return

    const movedUuids = new Set(
      [...candidaturesByEtape]
        .filter(([sourceEtapeUuid]) => sourceEtapeUuid !== targetColumnId)
        .flatMap(([sourceEtapeUuid, uuids]) => uuids.filter(uuid =>
          candidatures.value.some(c => c.uuid === uuid && c.etape.etape_uuid === sourceEtapeUuid),
        )),
    )

    if (movedUuids.size === 0)
      return

    assignEtape(movedUuids, etape)
    void persistEtapeChange(targetColumnId, [...movedUuids], previous, motifRefus)
  }

  const filters = useCandidaturesFilters({
    recrutementEtapes,
    candidatureKanban,
    candidatures,
  })

  watch(recrutementUuid, () => {
    filters.reset()
  })

  return {
    organismeUuid,
    recrutementUuid,
    recrutementDetail,
    intitule,
    findCandidature,
    candidatures,
    candidatureKanban,
    recrutementEtapes,
    totalCount,
    pendingDetail,
    pendingCandidatures,
    error,
    moveCandidature,
    moveCandidaturesBatch,
    filters,
  }
})
