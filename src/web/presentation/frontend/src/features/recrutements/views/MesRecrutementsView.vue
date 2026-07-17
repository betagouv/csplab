<script setup lang="ts">
import type {
  RecrutementKey,
} from '../types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from '../columns'
import RecrutementsFiltersDrawer from '../components/RecrutementsFiltersDrawer.vue'
import { useRecrutements } from '../composables/useRecrutements'

import { useRecrutementsFilters } from '../composables/useRecrutementsFilters'

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
  pending: recrutementsPending,
  error: recrutementsError,
  data: recrutementsData,
  load: loadRecrutements,
  has: hasRecrutements,
} = useRecrutements(TEMP_ORGANISME_UUID)

onMounted(() => {
  watch(activeTab, (newTab) => {
    if (!hasRecrutements(newTab)) {
      void loadRecrutements(newTab)
    }
  }, { immediate: true })
})

const router = useRouter()

function openOffre(recrutementUuid: string) {
  void router.push({ name: 'recrutement-candidatures-kanban', params: { recrutementUuid } })
}

const recrutementsActifsPage = ref(1)
const recrutementsArchivesPage = ref(1)

const PAGE_SIZE = 6
const {
  draft: filtersDraft,
  canReset: canResetFilters,
  syncDraft: syncFiltersDraft,
  apply: applyFiltersDraft,
  reset: resetFilters,
  search,
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

watch(filteredActifs, () => {
  recrutementsActifsPage.value = 1
})

watch(filteredArchives, () => {
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
  <CspPageContainer class="mes-recrutement-view">
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
        v-if="recrutementsPending"
        class="mes-recrutement-view__loading"
      >
        Chargement des recrutements...
      </div>
      <div
        v-else-if="recrutementsError"
        class="mes-recrutement-view__error"
      >
        Une erreur est survenue lors du chargement des recrutements.
      </div>
      <div v-else>
        <div class="mes-recrutement-view__toolbar">
          <p class="mes-recrutement-view__count">
            {{ countLabel }}
          </p>
          <div class="mes-recrutement-view__actions">
            <CspInput
              v-model="search"
              type="search"
              aria-label="Rechercher un recrutement"
              placeholder="Rechercher une offre, un candidat,…"
              class="mes-recrutement-view__search"
            />
            <CspButton
              :label="activeFiltersCount ? `Filtres (${activeFiltersCount})` : 'Filtres'"
              variant="tertiary"
              icon="ri:filter-line"
              is-icon-left
              @click="openFilters"
            />
          </div>
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
  </CspPageContainer>
</template>

<style scoped lang="scss">
.mes-recrutement-view__header {
  margin-bottom: var(--csp-space-4);
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

.mes-recrutement-view__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.75rem;
}

.mes-recrutement-view__search {
  min-width: 32rem;
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
