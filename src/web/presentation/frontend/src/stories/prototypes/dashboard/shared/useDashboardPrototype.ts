import type { AtsPage } from './AtsShell.vue'
import { computed, ref } from 'vue'
import {
  createRecrutements,
  createRecrutementsJourneeCalme,
  createTaches,
  createTachesJourneeCalme,
} from '../data/dashboardMock'

export type DashboardScenario = 'normal' | 'calme'

// État partagé par les deux dispositions (colonnes / empilée) : navigation entre
// les 3 pages du menu, ouverture des fiches détail, bascule d'une tâche faite/à faire.
export function useDashboardPrototype(scenario: DashboardScenario) {
  const recrutements = ref(scenario === 'calme' ? createRecrutementsJourneeCalme() : createRecrutements())
  const taches = ref(scenario === 'calme' ? createTachesJourneeCalme() : createTaches())

  const page = ref<AtsPage>('dashboard')
  const focusRecrutementId = ref<string | null>(null)
  const openRecrutementId = ref<string | null>(null)
  const openTacheId = ref<string | null>(null)

  const selectedRecrutement = computed(() =>
    recrutements.value.find(r => r.id === openRecrutementId.value) ?? null,
  )
  const selectedTache = computed(() =>
    taches.value.find(t => t.id === openTacheId.value) ?? null,
  )

  function navigate(target: AtsPage) {
    focusRecrutementId.value = null
    page.value = target
  }

  function openRecrutement(id: string) {
    openRecrutementId.value = id
  }

  function closeRecrutementDialog() {
    openRecrutementId.value = null
  }

  function voirCandidatures(id: string) {
    focusRecrutementId.value = id
    openRecrutementId.value = null
    page.value = 'recrutements'
  }

  function openTache(id: string) {
    openTacheId.value = id
  }

  function closeTacheDialog() {
    openTacheId.value = null
  }

  function toggleFait(id: string) {
    const tache = taches.value.find(t => t.id === id)
    if (tache)
      tache.fait = !tache.fait
  }

  function voirRecrutementDepuisTache(id: string) {
    openTacheId.value = null
    openRecrutementId.value = id
  }

  return {
    recrutements,
    taches,
    page,
    focusRecrutementId,
    selectedRecrutement,
    selectedTache,
    navigate,
    openRecrutement,
    closeRecrutementDialog,
    voirCandidatures,
    openTache,
    closeTacheDialog,
    toggleFait,
    voirRecrutementDepuisTache,
  }
}
