<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import CandidaturesFiltersDrawer from '../components/CandidaturesFiltersDrawer.vue'
import CandidaturesViewSwitch from '../components/CandidaturesViewSwitch.vue'
import { provideCandidaturesFilters } from '../composables/useCandidaturesFilters'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const route = useRoute()
const { recrutementDetail, etapes, pending: pendingDetail, error } = useRecrutementDetail(() => props)

const filters = provideCandidaturesFilters(etapes)

watch(() => props.recrutementUuid, () => {
  filters.reset()
  filters.listeSort.value = null
})

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

const loadFailed = computed(() => !pendingDetail.value && Boolean(error.value))

const isNotFound = computed(() =>
  !pendingDetail.value && !error.value && !recrutementDetail.value,
)

const currentView = computed(() => route.meta.candidaturesView ?? 'kanban')
</script>

<template>
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
    <CspTableToolbar :bordered="false">
      <template #status>
        <CandidaturesViewSwitch
          :organisme-uuid="organismeUuid"
          :recrutement-uuid="recrutementUuid"
          :current="currentView"
        />
      </template>
      <CspSearchBar
        v-model="search"
        mode="live"
        label="Rechercher un candidat"
        hide-label
        placeholder="Rechercher un candidat…"
        class="candidatures-search"
        @search="filters.flushSearch()"
      />
      <CspButton
        :label="activeFiltersCount ? `Filtres (${activeFiltersCount})` : 'Filtres'"
        variant="tertiary"
        icon="ri:filter-line"
        is-icon-left
        @click="openFilters"
      />
    </CspTableToolbar>
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

<style scoped lang="scss">
.candidatures-search {
  min-width: 20rem;
}
</style>
