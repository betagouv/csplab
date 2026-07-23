<script setup lang="ts">
import type {
  RecrutementKey,
} from '../types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
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
  pendingActifs,
  pendingArchives,
  error: recrutementsError,
  data: recrutementsData,
} = useRecrutements(TEMP_ORGANISME_UUID, activeTab)

const showActifsSkeleton = useMinimumPending(pendingActifs, 300)
const showArchivesSkeleton = useMinimumPending(pendingArchives, 300)

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
  <CspPageHeader
    title="Mes recrutements"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <p class="mes-recrutement-view__subtitle">
        Retrouvez ici l’ensemble de vos recrutements en cours et archivés.
      </p>
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    class="mes-recrutement-view"
    :tabs="TABS"
  >
    <template #shared>
      <div
        v-if="recrutementsError"
        class="mes-recrutement-view__error"
      >
        Une erreur est survenue lors du chargement des recrutements.
      </div>
      <template v-else>
        <div
          class="mes-recrutement-view__toolbar"
        >
          <CspSkeleton
            v-if="showActifsSkeleton || showArchivesSkeleton"
            class="mes-recrutement-view__count-skeleton"
            width="12rem"
            height="0.9375rem"
          />
          <p
            v-else
            class="mes-recrutement-view__count"
          >
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
      </template>
    </template>
    <template
      v-if="!recrutementsError"
      #tab-actifs
    >
      <div
        v-if="showActifsSkeleton"
        role="status"
        aria-label="Chargement des recrutements en cours"
      >
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="6"
          with-footer
        />
      </div>
      <CspDataTable
        v-else
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
              # · À traiter · En cours
            </span>
          </div>
        </template>
      </CspDataTable>
    </template>
    <template
      v-if="!recrutementsError"
      #tab-archives
    >
      <div
        v-if="showArchivesSkeleton"
        role="status"
        aria-label="Chargement des offres archivées"
      >
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="6"
          with-footer
        />
      </div>
      <CspDataTable
        v-else
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
  </CspPageContainer>
</template>

<style scoped lang="scss">
.mes-recrutement-view__error {
  color: var(--text-default-error);
}

.mes-recrutement-view__subtitle {
  margin: 0;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.mes-recrutement-view__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__count-skeleton {
  margin: 0.15rem 0;
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
  max-height: 1rem;
  & > span:first-child {
    margin-top: -0.75rem;
  }
}

.mes-recrutement-view__candidatures-legend {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
