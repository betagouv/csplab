<script setup lang="ts">
import type {
  RecrutementKey,
} from './types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, onMounted, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDisclosure } from '@/composables/useDisclosure'
import AtsAppShell from '../components/AtsAppShell.vue'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from './columns'
import RecrutementsFiltersDrawer from './components/RecrutementsFiltersDrawer.vue'
import { useRecrutements } from './useRecrutements'
import { useRecrutementsFilters } from './useRecrutementsFilters'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements' },
]

const activeTab = ref<RecrutementKey>('actifs')

const TABS: CspTabItem[] = [
  { value: 'actifs', label: 'Recrutements en cours' },
  { value: 'archives', label: 'Offres archivées' },
]
const {
  state: recrutementsState,
  data: recrutementsData,
  load: loadRecrutements,
  has: hasRecrutements,
} = useRecrutements({ source: 'mock' })

onMounted(() => {
  watch(activeTab, (newTab) => {
    if (!hasRecrutements(newTab)) {
      void loadRecrutements(newTab)
    }
  }, { immediate: true })
})

function openOffre(offreUuid: string) {
  // eslint-disable-next-line no-console
  console.log('openOffre', offreUuid)
}

const recrutementsActifsPage = ref(1)
const recrutementsArchivesPage = ref(1)

const PAGE_SIZE = 6
const {
  draft: filtersDraft,
  applied: appliedFilters,
  canReset: canResetFilters,
  syncDraft: syncFiltersDraft,
  apply: applyFiltersDraft,
  reset: resetFilters,
  filteredActifs,
  filteredArchives,
  activeFiltersCount,
  responsableOptions,
} = useRecrutementsFilters(recrutementsData)

const {
  isOpen: isFiltersDrawerOpen,
  open: openFiltersDrawer,
  close: closeFiltersDrawer,
} = useDisclosure()

function openFilters() {
  syncFiltersDraft()
  openFiltersDrawer()
}

function applyFilters() {
  applyFiltersDraft()
  closeFiltersDrawer()
}

watch(appliedFilters, () => {
  recrutementsActifsPage.value = 1
  recrutementsArchivesPage.value = 1
})

const countLabel = computed(() => {
  if (activeTab.value === 'actifs') {
    const count = filteredActifs.value.length
    return `${count} recrutement${count > 1 ? 's' : ''} en cours`
  }
  const count = filteredArchives.value.length
  return `${count} offre${count > 1 ? 's' : ''} archivée${count > 1 ? 's' : ''}`
})
</script>

<template>
  <AtsAppShell>
    <div class="mes-recrutement-view">
      <CspPageHeader
        title="Mes recrutements"
        :breadcrumb="BREADCRUMB"
        class="mes-recrutement-view__header"
      />
      <CspTabs
        v-model="activeTab"
      >
        <CspTabsList :tabs="TABS" />
        <div
          v-if="(
            recrutementsState === 'idle'
            || recrutementsState === 'loading'
          )"
          class="mes-recrutement-view__loading"
        >
          Chargement des recrutements...
        </div>
        <div
          v-else-if="recrutementsState === 'error'"
          class="mes-recrutement-view__error"
        >
          Une erreur est survenue lors du chargement des recrutements.
        </div>
        <div v-else>
          <div class="mes-recrutement-view__toolbar">
            <p class="mes-recrutement-view__count">
              {{ countLabel }}
            </p>
            <CspButton
              :label="activeFiltersCount ? `Filtres (${activeFiltersCount})` : 'Filtres'"
              variant="tertiary"
              icon="ri:filter-line"
              is-icon-left
              @click="openFilters"
            />
          </div>
          <CspTabsPanels :tabs="TABS">
            <template #actifs>
              <CspDataTable
                v-model:page="recrutementsActifsPage"
                :rows="filteredActifs"
                :columns="RECRUTEMENTS_ACTIFS_COLUMNS"
                :row-key="row => row.offer_id"
                activation-mode="cell"
                caption="Recrutements en cours"
                empty-label="Aucun recrutement en cours"
                :page-size="PAGE_SIZE"
                @activate="openOffre"
              >
                <template #header-candidatures="{ label }">
                  <div class="mes-recrutement-view__candidatures-head">
                    <span>{{ label }}</span>
                    <span class="mes-recrutement-view__candidatures-legend">
                      # • À traiter • En cours
                    </span>
                  </div>
                </template>
              </CspDataTable>
            </template>

            <template #archives>
              <CspDataTable
                v-model:page="recrutementsArchivesPage"
                :rows="filteredArchives"
                :columns="RECRUTEMENTS_ARCHIVES_COLUMNS"
                :row-key="row => row.offer_id"
                activation-mode="cell"
                caption="Offres archivées"
                empty-label="Aucune offre archivée"
                :page-size="PAGE_SIZE"
                @activate="openOffre"
              />
            </template>
          </CspTabsPanels>
          <RecrutementsFiltersDrawer
            v-model:open="isFiltersDrawerOpen"
            v-model:responsable="filtersDraft.responsable"
            v-model:type-contrat="filtersDraft.typeContrat"
            v-model:kind-contrat="filtersDraft.kindContrat"
            :responsable-options="responsableOptions"
            :can-reset="canResetFilters"
            @apply="applyFilters"
            @reset="resetFilters"
          />
        </div>
      </CspTabs>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.mes-recrutement-view {
  padding: 2rem;
}

.mes-recrutement-view__idle,
.mes-recrutement-view__loading,
.mes-recrutement-view__error {
  padding: 1rem 0;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__error {
  color: var(--text-default-error);
}

.mes-recrutement-view__toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1rem;
}

.mes-recrutement-view__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__candidatures-head {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.mes-recrutement-view__candidatures-legend {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
