<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import CandidaturesFiltersDrawer from '../components/CandidaturesFiltersDrawer.vue'
import CandidaturesViewSwitch from '../components/CandidaturesViewSwitch.vue'
import { useCandidatures } from '../composables/useCandidatures'
import { formatRecrutementMeta } from '../format'

const route = useRoute()
const recrutementUuid = route.params.recrutementUuid as string

const {
  recrutementDetail,
  intitule,
  pending,
  error,
  filters,
} = useCandidatures()

const showTitleSkeleton = useMinimumPending(
  computed(() => pending.value && !intitule.value),
)
const showSubtitleSkeleton = useMinimumPending(
  computed(() => pending.value && !recrutementDetail.value),
)

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

const title = computed(() => intitule.value ?? 'Candidatures')

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  ...(intitule.value ? [{ label: intitule.value }] : []),
])

const metaItems = computed(() =>
  recrutementDetail.value ? formatRecrutementMeta(recrutementDetail.value) : [],
)

const loadFailed = computed(() => !pending.value && Boolean(error.value))

const isNotFound = computed(() =>
  !pending.value && !error.value && !recrutementDetail.value,
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
  <CspPageHeader
    :breadcrumb="breadcrumb"
    :title="title"
    :back-link="{ to: { name: 'mes-recrutements' }, label: 'Retour à mes recrutements' }"
    :show-title-skeleton="showTitleSkeleton"
    :show-subtitle-skeleton="showSubtitleSkeleton"
  >
    <template #subtitle>
      <CspMetaList :items="metaItems" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    fill
    width="full"
    class="candidatures-view"
    :tabs="TABS"
  >
    <template #tab-candidatures>
      <CspErrorState
        v-if="loadFailed"
        title="Une erreur est survenue lors du chargement du recrutement."
      />

      <CspEmptyState
        v-else-if="isNotFound"
        icon="ri:search-line"
        title="Recrutement introuvable"
        description="Ce recrutement n'existe pas ou n'est plus accessible."
      />

      <template v-else>
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
    </template>
    <template #tab-activites-et-taches>
      <div class="candidatures-view__placeholder">
        Activités et tâches (à venir)
      </div>
    </template>
  </CspPageContainer>
</template>

<style scoped lang="scss">
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
  color: var(--text-mention-grey);
}
</style>
