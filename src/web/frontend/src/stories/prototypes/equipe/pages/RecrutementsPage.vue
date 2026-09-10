<script setup lang="ts">
import type { AjoutMembreResultat } from '../components/AjoutMembreDrawer.vue'
import type { ProtoRecrutement } from '../data/mock'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import ElapsedDaysCell from '@/components/base/CspDataTable/cells/ElapsedDaysCell.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { pluralize } from '@/utils/format'
import AjoutMembreDrawer from '../components/AjoutMembreDrawer.vue'
import CandidaturesCell from '../components/cells/CandidaturesCell.vue'
import IntituleCell from '../components/cells/IntituleCell.vue'
import OffreActionsCell from '../components/cells/OffreActionsCell.vue'
import ResponsablesCell from '../components/cells/ResponsablesCell.vue'
import { useEquipePrototypeContext } from '../shared/context'
import { formatAgentNom } from '../shared/format'

const proto = useEquipePrototypeContext()

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements' },
]

type Tab = 'actifs' | 'archives'

const TABS: CspTabItem<Tab>[] = [
  { value: 'actifs', label: 'En cours', icon: 'ri:briefcase-line' },
  { value: 'archives', label: 'Archivés', icon: 'ri:archive-line' },
]

const PAGE_SIZE = 6

const activeTab = ref<Tab>('actifs')
const page = ref(1)
const selectedIds = ref(new Set<string>())
const sansResponsableSeulement = ref(false)

const showSkeleton = useMinimumPending(proto.pending)

function responsablesLabel(row: ProtoRecrutement): string {
  return proto.responsablesDe(row).map(formatAgentNom).join(', ')
}

const COLUMNS_ACTIFS: CspColumnDef<ProtoRecrutement>[] = [
  { id: 'intitule', header: 'Intitulé de l\'offre', accessor: row => row.intitule, cellComponent: IntituleCell },
  { id: 'reference', header: 'Référence CSP', width: '9rem', accessor: row => row.reference },
  { id: 'datePublication', header: 'Publication', sortable: true, width: '8rem', accessor: row => row.datePublication, cellComponent: ElapsedDaysCell },
  { id: 'responsables', header: 'Responsable', sortable: true, width: '14rem', accessor: responsablesLabel, cellComponent: ResponsablesCell },
  { id: 'derniereActivite', header: 'Dernière activité', sortable: true, width: '9rem', wrapHeader: true, accessor: row => row.derniereActivite, cellComponent: ElapsedDaysCell },
  { id: 'candidatures', header: 'Candidatures actives', width: '9.5rem', wrapHeader: true, accessor: row => row.candidatures.total, cellComponent: CandidaturesCell },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]

const COLUMNS_ARCHIVES: CspColumnDef<ProtoRecrutement>[] = [
  { id: 'intitule', header: 'Intitulé de l\'offre', accessor: row => row.intitule, cellComponent: IntituleCell },
  { id: 'reference', header: 'Référence CSP', width: '9rem', accessor: row => row.reference },
  { id: 'responsables', header: 'Responsable', sortable: true, width: '14rem', accessor: responsablesLabel, cellComponent: ResponsablesCell },
  { id: 'derniereActivite', header: 'Dernière activité', sortable: true, width: '9rem', wrapHeader: true, accessor: row => row.derniereActivite, cellComponent: ElapsedDaysCell },
  { id: 'candidatures', header: 'Candidatures reçues', align: 'end', width: '8rem', wrapHeader: true, accessor: row => row.candidatures.total },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: OffreActionsCell },
]

const actifs = computed(() => proto.recrutementsVisibles.value.filter(r => !r.archive))
const archives = computed(() => proto.recrutementsVisibles.value.filter(r => r.archive))

const { search, filtered: actifsRecherches } = useTextSearch(actifs, row => [row.intitule, row.reference, responsablesLabel(row)])
const { search: searchArchives, filtered: archivesRecherchees } = useTextSearch(archives, row => [row.intitule, row.reference, responsablesLabel(row)])

const actifsFiltres = computed(() =>
  sansResponsableSeulement.value
    ? actifsRecherches.value.filter(r => proto.responsablesDe(r).length === 0)
    : actifsRecherches.value,
)

const sansResponsableCount = computed(() => proto.recrutementsSansResponsable.value.length)

watch([actifsFiltres, activeTab], () => {
  page.value = 1
})

watch(sansResponsableCount, (count) => {
  if (count === 0)
    sansResponsableSeulement.value = false
})

const actifsCountLabel = computed(() => {
  const count = actifsFiltres.value.length
  return `${count} ${pluralize(count, 'recrutement')} en cours`
})

const archivesCountLabel = computed(() => {
  const count = archivesRecherchees.value.length
  return `${count} ${pluralize(count, 'offre archivée', 'offres archivées')}`
})

const selectionMode = computed(() => (proto.peutAssignerResponsables.value ? 'checkbox' : 'none'))

function toggleRow(id: string): void {
  const next = new Set(selectedIds.value)
  if (next.has(id))
    next.delete(id)
  else
    next.add(id)
  selectedIds.value = next
}

function toggleAll(visibleIds: string[]): void {
  const allSelected = visibleIds.every(id => selectedIds.value.has(id))
  const next = new Set(selectedIds.value)
  for (const id of visibleIds) {
    if (allSelected)
      next.delete(id)
    else
      next.add(id)
  }
  selectedIds.value = next
}

function clearSelection(): void {
  selectedIds.value = new Set()
}

const assignationOpen = computed({
  get: () => proto.assignation.value !== null,
  set: (open) => {
    if (!open)
      proto.assignation.value = null
  },
})

const assignationUuids = computed({
  get: () => proto.assignation.value ?? [],
  set: (uuids) => {
    proto.assignation.value = uuids.length ? uuids : null
  },
})

function assignerSelection(): void {
  proto.demanderAssignation([...selectedIds.value])
}

function handleAssignation(resultat: AjoutMembreResultat): void {
  const uuids = assignationUuids.value
  const agentUuid = resultat.type === 'agent'
    ? resultat.agentUuid
    : proto.inviterALaVolee(resultat.invitation, uuids[0]).uuid
  proto.assignerResponsable(uuids, agentUuid, resultat.fonction)
  proto.assignation.value = null
  clearSelection()
}
</script>

<template>
  <CspPageHeader
    title="Recrutements"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <p class="recrutements-page__subtitle">
        Retrouvez ici l'ensemble des recrutements en cours et archivés.
      </p>
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    :tabs="TABS"
  >
    <template #tab-actifs>
      <CspTableToolbar
        :bordered="false"
        :selection-count="selectedIds.size"
      >
        <template #status>
          <div class="recrutements-page__status">
            <p class="recrutements-page__count">
              {{ actifsCountLabel }}
            </p>
            <CspButton
              v-if="proto.peutAssignerResponsables.value && sansResponsableCount > 0"
              :label="`${sansResponsableCount} sans responsable`"
              variant="tertiary-no-outline"
              size="sm"
              :icon="sansResponsableSeulement ? 'ri:filter-off-line' : 'ri:error-warning-line'"
              is-icon-left
              :aria-pressed="sansResponsableSeulement"
              class="recrutements-page__filter"
              @click="sansResponsableSeulement = !sansResponsableSeulement"
            />
          </div>
        </template>
        <template #selection-actions>
          <CspButton
            label="Annuler la sélection"
            variant="tertiary-no-outline"
            @click="clearSelection"
          />
          <CspButton
            label="Assigner un responsable"
            icon="ri:user-add-line"
            is-icon-left
            @click="assignerSelection"
          />
        </template>
        <CspInput
          v-model="search"
          type="search"
          aria-label="Rechercher un recrutement"
          placeholder="Rechercher une offre, une référence…"
          class="recrutements-page__search"
        />
      </CspTableToolbar>
      <CspAsyncSection
        :pending="showSkeleton"
        loading-label="Chargement des recrutements en cours"
      >
        <template #skeleton>
          <CspSkeletonTable
            :rows="PAGE_SIZE"
            :columns="6"
            with-footer
          />
        </template>
        <CspDataTable
          v-model:page="page"
          :rows="actifsFiltres"
          :columns="COLUMNS_ACTIFS"
          :row-key="row => row.uuid"
          :selection-mode="selectionMode"
          :selected-ids="selectedIds"
          :selection-label="row => `Sélectionner ${row.intitule}`"
          caption="Recrutements en cours"
          :empty-label="sansResponsableSeulement ? 'Toutes les offres ont un responsable' : 'Aucun recrutement en cours'"
          :page-size="PAGE_SIZE"
          @toggle-row="toggleRow"
          @toggle-all="toggleAll"
        >
          <template #header-candidatures="{ label }">
            <div class="recrutements-page__candidatures-head">
              <span>{{ label }}</span>
              <span class="recrutements-page__candidatures-legend">
                # · À traiter · En cours
              </span>
            </div>
          </template>
        </CspDataTable>
      </CspAsyncSection>
    </template>
    <template #tab-archives>
      <CspTableToolbar
        :bordered="false"
        :count="archivesCountLabel"
      >
        <CspInput
          v-model="searchArchives"
          type="search"
          aria-label="Rechercher une offre archivée"
          placeholder="Rechercher une offre, une référence…"
          class="recrutements-page__search"
        />
      </CspTableToolbar>
      <CspAsyncSection
        :pending="showSkeleton"
        loading-label="Chargement des offres archivées"
      >
        <template #skeleton>
          <CspSkeletonTable
            :rows="2"
            :columns="5"
            with-footer
          />
        </template>
        <CspDataTable
          :rows="archivesRecherchees"
          :columns="COLUMNS_ARCHIVES"
          :row-key="row => row.uuid"
          caption="Offres archivées"
          empty-label="Aucune offre archivée"
          :page-size="PAGE_SIZE"
        />
      </CspAsyncSection>
    </template>
  </CspPageContainer>

  <AjoutMembreDrawer
    v-model:open="assignationOpen"
    v-model:recrutement-uuids="assignationUuids"
    contexte="responsable"
    peut-inviter
    @submit="handleAssignation"
  />
</template>

<style scoped lang="scss">
.recrutements-page__subtitle {
  margin: 0;
  color: var(--text-mention-grey);
}

.recrutements-page__status {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.recrutements-page__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.recrutements-page__filter {
  color: var(--text-default-warning);
}

.recrutements-page__search {
  min-width: 20rem;
}

.recrutements-page__candidatures-head {
  display: flex;
  flex-direction: column;
  max-height: 1rem;

  & > span:first-child {
    margin-top: -0.75rem;
  }
}

.recrutements-page__candidatures-legend {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
