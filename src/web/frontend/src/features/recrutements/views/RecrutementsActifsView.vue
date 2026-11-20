<script setup lang="ts">
import type { AssignationResponsableResultat, RecrutementsActifs } from '../types'
import type { ToastOptions } from '@/composables/ui/useToast'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref, useTemplateRef } from 'vue'
import { useRouter } from 'vue-router'
import { isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTableSelection } from '@/composables/data/useTableSelection'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { useToast } from '@/composables/ui/useToast'
import { formatAgentLabel } from '@/features/agents/format'
import { CANDIDATURES_VIEW_ROUTE_NAMES } from '@/router/names'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { pluralize } from '@/utils/format'
import { RECRUTEMENTS_ACTIFS_COLUMNS } from '../columns'
import AssignResponsableForm from '../components/AssignResponsableForm.vue'
import RecrutementsActifsFiltersDrawer from '../components/RecrutementsActifsFiltersDrawer.vue'
import { useAssignResponsable } from '../composables/useAssignResponsable'
import { useRecrutements } from '../composables/useRecrutements'
import { useRecrutementsFilters } from '../composables/useRecrutementsFilters'

const props = defineProps<{
  organismeUuid: string
}>()

const AUCUN_RECRUTEMENT_EN_COURS_DESCRIPTION = 'Les recrutements auxquels vous participez apparaissent ici. Pour accéder à un recrutement, contactez la personne responsable dans votre organisation.'

const router = useRouter()

const { canOnOrganisme } = useRouteOrganisme()
const canAssignResponsable = computed(() => canOnOrganisme('set_recrutements_responsable'))

const { pendingActifs, data: recrutementsData } = useRecrutements(() => props.organismeUuid, 'actifs')

const showActifsSkeleton = useMinimumPending(pendingActifs, 300)

function openOffre(recrutementUuid: string) {
  void router.push({
    name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
    params: { organismeUuid: props.organismeUuid, recrutementUuid },
  })
}

const recrutementsActifsPage = ref(1)

const actifsFilters = useRecrutementsFilters(computed(() => recrutementsData.actifs))

const actifsFiltersDrawer = useDisclosure()

const { addToast } = useToast()

const selection = useTableSelection(actifsFilters.filtered, row => row.uuid)
const assignationDrawer = useDisclosure()
const recrutementToAssign = ref<RecrutementsActifs | null>(null)
const recrutementsToAssign = computed(() =>
  recrutementToAssign.value ? [recrutementToAssign.value] : selection.selected.value,
)
const {
  status: responsableStatus,
  foundAgent,
  searching,
  search: searchResponsable,
  assign,
  submitting,
  reset: resetResponsable,
} = useAssignResponsable(() => props.organismeUuid)

const actifsTable = useTemplateRef<{ visibleIds: string[] }>('actifsTable')

const selectionLabel = computed(() => {
  const count = selection.count.value
  return `${count} ${pluralize(count, 'recrutement sélectionné', 'recrutements sélectionnés')}`
})

const selectionHint = computed(() => {
  const visibleIds = new Set(actifsTable.value?.visibleIds ?? [])
  const elsewhere = selection.selected.value.filter(row => !visibleIds.has(row.uuid)).length
  return elsewhere > 0
    ? `dont ${elsewhere} ${pluralize(elsewhere, 'sur une autre page', 'sur d’autres pages')}`
    : undefined
})

function assignationToast(
  resultat: AssignationResponsableResultat,
  agent: AgentRecherche | null,
): ToastOptions {
  const nom = agent ? formatAgentLabel(agent) : 'Le membre choisi'
  const reussites = resultat.reussites.length
  const assignees = `${nom} est responsable de ${reussites} ${pluralize(reussites, 'recrutement')}`

  if (resultat.echecs.length === 0) {
    return {
      variant: 'success',
      title: 'Responsable assigné',
      description: `${assignees}.`,
    }
  }
  const echecs = resultat.echecs.length
  return {
    variant: 'warning',
    title: 'Assignation partielle',
    description: `${assignees}, ${echecs} ${pluralize(echecs, 'recrutement ignoré', 'recrutements ignorés')}.`,
  }
}

function assignationErrorTitle(assignationError: unknown): string {
  if (isHttpStatus(assignationError, 403)) {
    return 'Vous n\'avez pas les droits pour assigner un responsable'
  }
  if (isHttpStatus(assignationError, 404)) {
    return 'Ce membre n\'est plus rattaché à l\'organisme'
  }
  return 'L\'assignation du responsable a échoué'
}

function openAssignment(recrutement: RecrutementsActifs | null = null) {
  recrutementToAssign.value = recrutement
  resetResponsable()
  assignationDrawer.open()
}

function removeFromAssignment(recrutementUuid: string) {
  if (recrutementToAssign.value) {
    assignationDrawer.close()
    return
  }
  selection.toggle(recrutementUuid)
  if (selection.count.value === 0) {
    assignationDrawer.close()
  }
}

async function handleAssign() {
  const recrutementIds = recrutementsToAssign.value.map(row => row.uuid)

  try {
    const resultat = await assign(recrutementIds)
    const agent = foundAgent.value
    assignationDrawer.close()
    if (!recrutementToAssign.value) {
      selection.clear()
    }
    addToast(assignationToast(resultat, agent))
  }
  catch (assignationError) {
    addToast({ variant: 'error', title: assignationErrorTitle(assignationError) })
  }
}

function openActifsFilters() {
  actifsFilters.syncDraft()
  actifsFiltersDrawer.open()
}

function applyActifsFilters() {
  actifsFilters.apply()
  actifsFiltersDrawer.close()
}

const aucunRecrutementActif = computed(
  () => !showActifsSkeleton.value && recrutementsData.actifs.length === 0,
)

const actifsCountLabel = computed(() => {
  const count = actifsFilters.filtered.value.length
  return `${count} ${pluralize(count, 'recrutement')} en cours`
})
</script>

<template>
  <CspEmptyState
    v-if="aucunRecrutementActif"
    icon="ri:briefcase-line"
    title="Vous n’avez pas de recrutement en cours"
    :description="AUCUN_RECRUTEMENT_EN_COURS_DESCRIPTION"
  />
  <template v-else>
    <CspTableToolbar
      :bordered="false"
      :count="actifsCountLabel"
      :pending="showActifsSkeleton"
      :selection-count="selection.count.value"
      :selection-label="selectionLabel"
      :selection-hint="selectionHint"
    >
      <template #selection-actions>
        <CspButton
          label="Assigner un responsable"
          @click="openAssignment()"
        />
      </template>
      <CspSearchBar
        v-model="actifsFilters.search.value"
        mode="live"
        label="Rechercher un recrutement"
        hide-label
        placeholder="Intitulé, référence, responsable…"
      />
      <CspButton
        :label="actifsFilters.activeFiltersCount.value ? `Filtres (${actifsFilters.activeFiltersCount.value})` : 'Filtres'"
        variant="tertiary"
        icon="ri:filter-line"
        is-icon-left
        @click="openActifsFilters"
      />
    </CspTableToolbar>
    <RecrutementsActifsFiltersDrawer
      v-model:open="actifsFiltersDrawer.isOpen.value"
      v-model:responsable="actifsFilters.draft.responsable"
      :responsable-options="actifsFilters.responsableOptions.value"
      :can-reset="actifsFilters.canReset.value"
      @apply="applyActifsFilters"
      @reset="actifsFilters.reset()"
    />
    <CspDrawer
      v-model:open="assignationDrawer.isOpen.value"
      title="Assigner un responsable"
      size="md"
    >
      <AssignResponsableForm
        :recrutements="recrutementsToAssign"
        :status="responsableStatus"
        :agent="foundAgent"
        :searching="searching"
        :submitting="submitting"
        @remove="removeFromAssignment"
        @search="searchResponsable"
        @assign="handleAssign"
        @reset="resetResponsable"
        @cancel="assignationDrawer.close()"
      />
    </CspDrawer>
    <CspAsyncSection
      :pending="showActifsSkeleton"
      loading-label="Chargement des recrutements en cours"
    >
      <template #skeleton>
        <CspSkeletonTable
          :columns="RECRUTEMENTS_ACTIFS_COLUMNS.length"
        />
      </template>
      <CspDataTable
        ref="actifsTable"
        v-model:page="recrutementsActifsPage"
        :rows="actifsFilters.filtered.value"
        :columns="RECRUTEMENTS_ACTIFS_COLUMNS"
        :row-key="row => row.uuid"
        :selection-mode="canAssignResponsable ? 'checkbox' : 'none'"
        :selected-ids="selection.selectedIds.value"
        :selection-label="row => `Sélectionner ${row.intitule}`"
        activation-mode="cell"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="TABLE_PAGE_SIZE"
        @activate="openOffre"
        @toggle-row="selection.toggle"
        @toggle-all="selection.toggleVisible"
      >
        <template #cell-responsables="{ row, value }">
          <CspButton
            v-if="canAssignResponsable && row.responsables.length === 0"
            label="Assigner un responsable"
            variant="secondary"
            size="sm"
            :aria-label="`Assigner un responsable à ${row.intitule}`"
            @click="openAssignment(row)"
          />
          <template v-else>
            {{ value }}
          </template>
        </template>
      </CspDataTable>
    </CspAsyncSection>
  </template>
</template>
