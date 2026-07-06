import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../api/recrutement'
import { readonly, ref } from 'vue'
import { runAsyncAction } from '@/composables/useAsyncState'
import { getEtapesRecrutement, initEtapesRecrutement, updateEtapesRecrutement } from '../api/recrutement'

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
  const etapes = ref<EtapeRecrutement[]>([])
  const loading = ref(true)
  const saving = ref(false)
  const error = ref<Error | null>(null)

  function isEtapeLocked(etape: EtapeRecrutement): boolean {
    return etape.categorie !== 'EN_COURS'
  }

  async function fetchEtapes(): Promise<void> {
    await runAsyncAction(loading, error, async () => {
      etapes.value = await getEtapesRecrutement(organismeUuid)
    })
  }

  async function saveEtapes(nouvellesEtapes: EtapeRecrutement[]): Promise<void> {
    await runAsyncAction(saving, error, async () => {
      etapes.value = await updateEtapesRecrutement(
        organismeUuid,
        toUpdatePayload(nouvellesEtapes),
      )
    })
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
    await runAsyncAction(saving, error, async () => {
      etapes.value = await initEtapesRecrutement(organismeUuid)
    })
  }

  return {
    etapes,
    loading: readonly(loading),
    saving: readonly(saving),
    error: readonly(error),
    isEtapeLocked,
    fetchEtapes,
    reorderEtapes,
    addEtape,
    addEtapeAt,
    renameEtape,
    removeEtape,
    resetEtapes,
  }
}
