import type { ProtoCandidature, ProtoEtape, ProtoNote } from '../data/mock'
import { computed, reactive, ref } from 'vue'
import { createScenario, minutesAgo, nextUuid, UTILISATEUR } from '../data/mock'

export type PanelTab = 'candidature' | 'historique' | 'documents' | 'notes' | 'messages'

export interface PanelPosition {
  index: number
  total: number
  previousUuid: string | null
  nextUuid: string | null
}

export interface EtapeToast {
  candidatureUuid: string
  candidatNom: string
  etapeNom: string
}

export interface InfoToast {
  title: string
  description?: string
}

export type InitialOpen = 'aucune' | 'premiere' | 'derniere' | 'sans-cv' | 'cv-illisible'

export function useCandidaturePrototype(initialOpen: InitialOpen = 'aucune') {
  const scenario = reactive(createScenario())

  const openUuid = ref<string | null>(null)
  const contextEtapeUuid = ref<string | null>(null)
  const tab = ref<PanelTab>('candidature')
  const noteDraft = ref('')
  const notePrivee = ref(false)
  const tagPickerOpen = ref(false)
  const pendingAction = ref<(() => void) | null>(null)
  const etapeToast = ref<EtapeToast | null>(null)
  const infoToast = ref<InfoToast | null>(null)

  const candidature = computed<ProtoCandidature | null>(
    () => scenario.candidatures.find(c => c.uuid === openUuid.value) ?? null,
  )

  function etapeOf(uuid: string): ProtoEtape | null {
    return scenario.etapes.find(e => e.candidatureUuids.includes(uuid)) ?? null
  }

  function candidatureOf(uuid: string): ProtoCandidature | null {
    return scenario.candidatures.find(c => c.uuid === uuid) ?? null
  }

  const etapeCourante = computed(() => (openUuid.value ? etapeOf(openUuid.value) : null))

  const position = computed<PanelPosition | null>(() => {
    const etape = scenario.etapes.find(e => e.uuid === contextEtapeUuid.value)
    if (!etape || !openUuid.value)
      return null
    const uuids = etape.candidatureUuids
    const index = uuids.indexOf(openUuid.value)
    if (index === -1)
      return null
    return {
      index,
      total: uuids.length,
      previousUuid: uuids[index - 1] ?? null,
      nextUuid: uuids[index + 1] ?? null,
    }
  })

  const hasDraft = computed(() => noteDraft.value.trim().length > 0 || tagPickerOpen.value)

  function resetDraft(): void {
    noteDraft.value = ''
    notePrivee.value = false
    tagPickerOpen.value = false
  }

  function guarded(action: () => void): void {
    if (hasDraft.value) {
      pendingAction.value = action
      return
    }
    action()
  }

  function continueEditing(): void {
    pendingAction.value = null
  }

  function quitWithoutSaving(): void {
    const action = pendingAction.value
    pendingAction.value = null
    resetDraft()
    action?.()
  }

  function open(uuid: string): void {
    contextEtapeUuid.value = etapeOf(uuid)?.uuid ?? null
    openUuid.value = uuid
    tab.value = 'candidature'
    resetDraft()
  }

  function close(): void {
    guarded(() => {
      openUuid.value = null
      contextEtapeUuid.value = null
      resetDraft()
    })
  }

  function goPrevious(): void {
    const uuid = position.value?.previousUuid
    if (uuid)
      guarded(() => open(uuid))
  }

  function goNext(): void {
    const uuid = position.value?.nextUuid
    if (uuid)
      guarded(() => open(uuid))
  }

  function logActivite(target: ProtoCandidature, input: Omit<ProtoCandidature['activites'][number], 'uuid' | 'date'>): void {
    target.activites.unshift({ uuid: nextUuid('act'), date: minutesAgo(0), ...input })
  }

  function changerEtape(targetEtapeUuid: string): void {
    guarded(() => {
      const current = candidature.value
      const source = etapeCourante.value
      const target = scenario.etapes.find(e => e.uuid === targetEtapeUuid)
      if (!current || !source || !target || source.uuid === target.uuid)
        return

      const index = source.candidatureUuids.indexOf(current.uuid)
      source.candidatureUuids.splice(index, 1)
      target.candidatureUuids.push(current.uuid)
      logActivite(current, {
        type: 'etape',
        auteur: UTILISATEUR.nom,
        libelle: `Déplacé de ${source.nom} à ${target.nom}`,
      })
      etapeToast.value = {
        candidatureUuid: current.uuid,
        candidatNom: `${current.candidat.prenom} ${current.candidat.nom}`,
        etapeNom: target.nom,
      }

      const following = source.candidatureUuids[index]
      if (following) {
        open(following)
        contextEtapeUuid.value = source.uuid
      }
      else {
        openUuid.value = null
        contextEtapeUuid.value = null
        resetDraft()
      }
    })
  }

  function revenirCandidature(): void {
    const toast = etapeToast.value
    etapeToast.value = null
    if (toast)
      guarded(() => open(toast.candidatureUuid))
  }

  function saveNote(): void {
    const current = candidature.value
    const message = noteDraft.value.trim()
    if (!current || !message)
      return
    current.notes.unshift({
      uuid: nextUuid('note'),
      auteur: UTILISATEUR.nom,
      role: 'Vous',
      date: minutesAgo(0),
      message,
      privee: notePrivee.value,
      mienne: true,
    })
    if (!notePrivee.value)
      logActivite(current, { type: 'note', auteur: UTILISATEUR.nom, libelle: 'Note enregistrée' })
    resetDraft()
    infoToast.value = { title: 'Note enregistrée', description: 'Retrouvez-la dans l\'onglet Notes.' }
  }

  function updateNote(uuid: string, patch: Partial<Pick<ProtoNote, 'message' | 'privee'>>): void {
    const note = candidature.value?.notes.find(n => n.uuid === uuid)
    if (note)
      Object.assign(note, patch)
  }

  function deleteNote(uuid: string): void {
    const current = candidature.value
    if (current)
      current.notes = current.notes.filter(n => n.uuid !== uuid)
  }

  function addTag(label: string): void {
    const current = candidature.value
    if (!current || current.tags.includes(label))
      return
    current.tags.push(label)
    logActivite(current, { type: 'tag', auteur: UTILISATEUR.nom, libelle: 'a ajouté un tag', tags: [label] })
    tagPickerOpen.value = false
  }

  function removeTag(label: string): void {
    const current = candidature.value
    if (!current)
      return
    current.tags = current.tags.filter(t => t !== label)
    logActivite(current, { type: 'tag', auteur: UTILISATEUR.nom, libelle: 'a retiré un tag', tags: [label] })
  }

  function copierLien(): void {
    infoToast.value = {
      title: 'Lien copié dans le presse papier',
      description: 'Vous pouvez coller le lien où vous le souhaitez.',
    }
  }

  const aTraiter = scenario.etapes[0]!
  const initialUuid = {
    'aucune': null,
    'premiere': aTraiter.candidatureUuids[0] ?? null,
    'derniere': aTraiter.candidatureUuids.at(-1) ?? null,
    'sans-cv': scenario.candidatures.find(c => c.cv === 'absent')?.uuid ?? null,
    'cv-illisible': scenario.candidatures.find(c => c.cv === 'illisible')?.uuid ?? null,
  }[initialOpen]
  if (initialUuid)
    open(initialUuid)

  return {
    scenario,
    candidature,
    candidatureOf,
    etapeOf,
    etapeCourante,
    position,
    tab,
    noteDraft,
    notePrivee,
    tagPickerOpen,
    hasDraft,
    pendingAction,
    etapeToast,
    infoToast,
    open,
    close,
    goPrevious,
    goNext,
    continueEditing,
    quitWithoutSaving,
    changerEtape,
    revenirCandidature,
    saveNote,
    updateNote,
    deleteNote,
    addTag,
    removeTag,
    copierLien,
  }
}

export type CandidaturePrototype = ReturnType<typeof useCandidaturePrototype>
