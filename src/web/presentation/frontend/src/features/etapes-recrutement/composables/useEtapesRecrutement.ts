import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed } from 'vue'
import { initEtapesRecrutement, updateEtapesRecrutement } from '../api'
import { etapesRecrutementQuery } from '../queries'

function toUpdatePayload(items: EtapeRecrutement[]): UpdateEtapeRecrutement[] {
  return items.map((etape) => {
    const payload: UpdateEtapeRecrutement = {
      nom: etape.nom,
      categorie: etape.categorie,
    }
    if (etape.etape_uuid) {
      payload.etape_uuid = etape.etape_uuid
    }
    return payload
  })
}

function buildNouvelleEtape(nom: string): EtapeRecrutement {
  return {
    etape_uuid: '',
    nom,
    categorie: 'EN_COURS',
  }
}

function insertEtape(
  etapes: EtapeRecrutement[],
  nouvelle: EtapeRecrutement,
): EtapeRecrutement[] {
  const finalIndex = etapes.findIndex(
    e => e.categorie === 'REFUS' || e.categorie === 'ACCEPTE',
  )
  const insertAt = finalIndex === -1 ? etapes.length : finalIndex
  return [...etapes.slice(0, insertAt), nouvelle, ...etapes.slice(insertAt)]
}

export function useEtapesRecrutement(organismeUuid: string) {
  const queryCache = useQueryCache()
  const queryOptions = etapesRecrutementQuery({ organismeUuid })
  const query = useQuery(queryOptions)

  const etapes = computed(() => query.data.value ?? [])

  function applyFreshEtapes(fresh: EtapeRecrutement[]): void {
    queryCache.setQueryData(queryOptions.key, fresh)
  }

  const update = useMutation({
    mutation: (payload: UpdateEtapeRecrutement[]) =>
      updateEtapesRecrutement(organismeUuid, payload),
    onSuccess: applyFreshEtapes,
  })

  const init = useMutation({
    mutation: () => initEtapesRecrutement(organismeUuid),
    onSuccess: applyFreshEtapes,
  })

  const loading = query.isPending
  const saving = computed(() => update.isLoading.value || init.isLoading.value)
  const error = computed(
    () => query.error.value ?? update.error.value ?? init.error.value,
  )

  function isEtapeLocked(etape: EtapeRecrutement): boolean {
    return etape.categorie !== 'EN_COURS'
  }

  async function saveEtapes(nouvellesEtapes: EtapeRecrutement[]): Promise<void> {
    await update.mutateAsync(toUpdatePayload(nouvellesEtapes)).catch(() => undefined)
  }

  async function reorderEtapes(nouvellesEtapes: EtapeRecrutement[]): Promise<void> {
    await saveEtapes(nouvellesEtapes)
  }

  async function addEtape(nom: string): Promise<void> {
    await saveEtapes(insertEtape(etapes.value, buildNouvelleEtape(nom)))
  }

  async function addEtapeAt(nom: string, index: number): Promise<void> {
    const nouvelle = buildNouvelleEtape(nom)
    const updated = [
      ...etapes.value.slice(0, index),
      nouvelle,
      ...etapes.value.slice(index),
    ]
    await saveEtapes(updated)
  }

  async function renameEtape(etapeUuid: string, nouveauNom: string): Promise<void> {
    const updated = etapes.value.map(e =>
      e.etape_uuid === etapeUuid ? { ...e, nom: nouveauNom } : e,
    )
    await saveEtapes(updated)
  }

  async function removeEtape(etapeUuid: string): Promise<void> {
    await saveEtapes(etapes.value.filter(e => e.etape_uuid !== etapeUuid))
  }

  async function resetEtapes(): Promise<void> {
    await init.mutateAsync().catch(() => undefined)
  }

  return {
    etapes,
    loading,
    saving,
    error,
    isEtapeLocked,
    reorderEtapes,
    addEtape,
    addEtapeAt,
    renameEtape,
    removeEtape,
    resetEtapes,
  }
}
