import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import type { OrganismeParams, RecrutementParams } from '@/api/params'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { recrutementKeys } from '@/api/queryKeys'
import { can } from '@/utils/authorizedActions'
import {
  initEtapesOffre,
  initEtapesRecrutement,
  updateEtapesOffre,
  updateEtapesRecrutement,
} from '../api'
import { etapesOffreQuery, etapesRecrutementQuery } from '../queries'

export type EtapesRecrutementType
  = | { type: 'organisme' } & OrganismeParams
    | { type: 'offre' } & RecrutementParams

function toUpdatePayload(items: EtapeRecrutement[]): UpdateEtapeRecrutement[] {
  return items.map(({ uuid, nom, categorie }) => ({ uuid, nom, categorie }))
}

function buildNouvelleEtape(nom: string): UpdateEtapeRecrutement {
  return { nom, categorie: 'EN_COURS' }
}

function resolveEtapesApi(params: EtapesRecrutementType) {
  if (params.type === 'offre') {
    const { organismeUuid, recrutementUuid } = params
    const recrutement = { organismeUuid, recrutementUuid }
    return {
      queryOptions: etapesOffreQuery(recrutement),
      update: (payload: UpdateEtapeRecrutement[]) => updateEtapesOffre(recrutement, payload),
      init: () => initEtapesOffre(recrutement),
      clesAffectees: [recrutementKeys.root(recrutement)],
    }
  }

  const organisme = { organismeUuid: params.organismeUuid }
  return {
    queryOptions: etapesRecrutementQuery(organisme),
    update: (payload: UpdateEtapeRecrutement[]) => updateEtapesRecrutement(organisme, payload),
    init: () => initEtapesRecrutement(organisme),
    clesAffectees: [],
  }
}

export function useEtapesRecrutement(params: EtapesRecrutementType) {
  const queryCache = useQueryCache()
  const etapesApi = resolveEtapesApi(params)
  const queryOptions = etapesApi.queryOptions
  const query = useQuery(queryOptions)

  const etapes = computed(() => query.data.value ?? [])

  const lastInsertableIndex = computed(() =>
    etapes.value.map(etape => can(etape.etape_actions, 'insert_etape_after')).lastIndexOf(true),
  )
  const canAddEtape = computed(() => lastInsertableIndex.value !== -1)

  function applyFreshEtapes(fresh: EtapeRecrutement[]): void {
    queryCache.setQueryData(queryOptions.key, fresh)
    const etapesEntry = queryCache.get(queryOptions.key)
    for (const key of etapesApi.clesAffectees) {
      void queryCache.invalidateQueries({ key, predicate: entry => entry !== etapesEntry })
    }
  }

  const update = useMutation({
    mutation: (payload: UpdateEtapeRecrutement[]) => etapesApi.update(payload),
    onSuccess: applyFreshEtapes,
  })

  const init = useMutation({
    mutation: () => etapesApi.init(),
    onSuccess: applyFreshEtapes,
  })

  const loading = query.isPending
  const saving = computed(() => update.isLoading.value || init.isLoading.value)
  const error = query.error

  async function saveEtapes(nouvellesEtapes: EtapeRecrutement[]): Promise<void> {
    await update.mutateAsync(toUpdatePayload(nouvellesEtapes))
  }

  async function reorderEtapes(nouvellesEtapes: EtapeRecrutement[]): Promise<void> {
    await saveEtapes(nouvellesEtapes)
  }

  async function addEtape(nom: string): Promise<void> {
    await addEtapeAt(nom, lastInsertableIndex.value + 1)
  }

  async function addEtapeAt(nom: string, index: number): Promise<void> {
    const payload = toUpdatePayload(etapes.value)
    await update.mutateAsync([
      ...payload.slice(0, index),
      buildNouvelleEtape(nom),
      ...payload.slice(index),
    ])
  }

  async function renameEtape(etapeUuid: string, nouveauNom: string): Promise<void> {
    const updated = etapes.value.map(e =>
      e.uuid === etapeUuid ? { ...e, nom: nouveauNom } : e,
    )
    await saveEtapes(updated)
  }

  async function removeEtape(etapeUuid: string): Promise<void> {
    await saveEtapes(etapes.value.filter(e => e.uuid !== etapeUuid))
  }

  async function resetEtapes(): Promise<void> {
    await init.mutateAsync()
  }

  return {
    etapes,
    loading,
    saving,
    error,
    canAddEtape,
    reorderEtapes,
    addEtape,
    addEtapeAt,
    renameEtape,
    removeEtape,
    resetEtapes,
  }
}
