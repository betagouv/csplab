<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import CandidaturesFiltersDrawer from '../components/CandidaturesFiltersDrawer.vue'
import CandidaturesViewSwitch from '../components/CandidaturesViewSwitch.vue'
import { provideCandidatures } from '../composables/useCandidatures'
import { formatRecrutementMeta } from '../format'

const route = useRoute()
const recrutementUuid = route.params.recrutementUuid as string

const {
  recrutementDetail,
  pending,
  error,
  filters,
} = provideCandidatures(TEMP_ORGANISME_UUID, recrutementUuid)

const {
  draft: filtersDraft,
  canReset: canResetFilters,
  search,
  activeFiltersCount,
  etapeOptions,
} = filters

const {
  isOpen: isFiltersDrawerOpen,
  open: openFiltersDrawer,
  close: closeFiltersDrawer,
} = useDisclosure()

function openFilters() {
  filters.syncDraft()
  openFiltersDrawer()
}

function applyFilters() {
  filters.apply()
  closeFiltersDrawer()
}

const title = computed(() => recrutementDetail.value?.intitule ?? 'Candidatures')

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  { label: title.value },
])

const metaItems = computed(() =>
  recrutementDetail.value ? formatRecrutementMeta(recrutementDetail.value) : [],
)

const isNotFound = computed(() =>
  !pending.value && (Boolean(error.value) || !recrutementDetail.value),
)

const currentView = computed(() => {
  return route.name === 'recrutement-candidatures-kanban' ? 'kanban' : 'liste'
})

const TABS: CspTabItem[] = [
  { value: 'candidatures', label: 'Candidatures' },
  { value: 'activites-et-taches', label: 'Activités et tâches' },
]
const activeTab = ref<'candidatures' | 'activites-et-taches'>('candidatures')
</script>

<template>
  <div class="candidatures-view">
    <CspPageHeader
      :title="title"
      :breadcrumb="breadcrumb"
      :back-to="{ name: 'mes-recrutements' }"
      back-label="Retour à mes recrutements"
      class="candidatures-view__header"
    />

    <CspMetaList
      v-if="recrutementDetail"
      :items="metaItems"
      class="candidatures-view__meta"
    />

    <div
      v-if="pending"
      class="candidatures-view__status"
    >
      Chargement des candidatures...
    </div>

    <div
      v-else-if="isNotFound"
      class="candidatures-view__status candidatures-view__status--error"
    >
      Recrutement introuvable.
    </div>

    <CspTabs
      v-else
      v-model="activeTab"
    >
      <CspTabsList :tabs="TABS" />
      <CspTabsPanels :tabs="TABS">
        <template #candidatures>
          <div class="candidatures-view__toolbar">
            <CandidaturesViewSwitch
              :recrutement-uuid="recrutementUuid"
              :current="currentView"
            />
            <div class="candidatures-view__actions">
              <CspInput
                v-model="search"
                type="search"
                aria-label="Rechercher un candidat"
                placeholder="Rechercher un candidat…"
                class="candidatures-view__search"
                @keydown.enter="filters.flushSearch()"
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
          <router-view />
          <CandidaturesFiltersDrawer
            v-model:open="isFiltersDrawerOpen"
            v-model:etapes="filtersDraft.etapes"
            :etape-options="etapeOptions"
            :can-reset="canResetFilters"
            @apply="applyFilters"
            @reset="filters.reset"
          />
        </template>
        <template #activites-et-taches>
          <div class="candidatures-view__placeholder">
            Activités et tâches (à venir)
          </div>
        </template>
      </CspTabsPanels>
    </CspTabs>
  </div>
</template>

<style scoped lang="scss">
.candidatures-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 2rem;
  box-sizing: border-box;
  overflow: hidden;
}

.candidatures-view__header {
  margin-bottom: var(--csp-space-4);
}

.candidatures-view__meta {
  margin-bottom: var(--csp-space-4);
}

.candidatures-view__status {
  padding: 1rem 0;
  color: var(--text-mention-grey);
}

.candidatures-view__status--error {
  color: var(--text-default-error);
}

.candidatures-view__toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: var(--csp-space-4);
}

.candidatures-view__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.75rem;
}

.candidatures-view__search {
  min-width: 32rem;
}

.candidatures-view__placeholder {
  padding: 2rem 0;
  color: var(--text-mention-grey);
}

.candidatures-view :deep(.csp-tabs) {
  flex: 1;
  min-height: 0;
}

.candidatures-view :deep(.csp-tabs__panels) {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.candidatures-view :deep(.csp-tabs__content) {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}
</style>
