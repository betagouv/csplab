<script setup lang="ts">
import type { DashboardScenario } from '../../shared/useDashboardPrototype'
import { computed } from 'vue'
import AtsShell from '../../shared/AtsShell.vue'
import RecrutementDetailDialog from '../../shared/RecrutementDetailDialog.vue'
import TacheDetailDialog from '../../shared/TacheDetailDialog.vue'
import { useDashboardPrototype } from '../../shared/useDashboardPrototype'
import MesRecrutementsView from '../../views/MesRecrutementsView.vue'
import MesTachesView from '../../views/MesTachesView.vue'
import TableauDeBordView from '../../views/TableauDeBordView.vue'

const props = withDefaults(defineProps<{
  // 'colonnes' = Mes recrutements et Mes tâches côte à côte
  // 'empile'   = les deux blocs empilés pleine largeur
  layout: 'colonnes' | 'empile'
  scenario?: DashboardScenario
}>(), {
  scenario: 'normal',
})

const {
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
} = useDashboardPrototype(props.scenario)

const isRecrutementDialogOpen = computed(() => selectedRecrutement.value !== null)
const isTacheDialogOpen = computed(() => selectedTache.value !== null)
</script>

<template>
  <AtsShell v-model:page="page">
    <TableauDeBordView
      v-if="page === 'dashboard'"
      user-first-name="Alice"
      :recrutements="recrutements"
      :taches="taches"
      :layout="layout"
      @navigate="navigate"
      @open-recrutement="openRecrutement"
      @open-tache="openTache"
      @toggle-fait="toggleFait"
    />
    <MesRecrutementsView
      v-else-if="page === 'recrutements'"
      :recrutements="recrutements"
      :focus-recrutement-id="focusRecrutementId"
      @open="openRecrutement"
    />
    <MesTachesView
      v-else
      :taches="taches"
      @open="openTache"
      @toggle-fait="toggleFait"
    />
  </AtsShell>

  <RecrutementDetailDialog
    :open="isRecrutementDialogOpen"
    :recrutement="selectedRecrutement"
    @update:open="value => !value && closeRecrutementDialog()"
    @voir-candidatures="voirCandidatures"
  />

  <TacheDetailDialog
    :open="isTacheDialogOpen"
    :tache="selectedTache"
    @update:open="value => !value && closeTacheDialog()"
    @toggle-fait="toggleFait"
    @voir-recrutement="voirRecrutementDepuisTache"
  />
</template>
