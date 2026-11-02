<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { useCandidaturesFilters } from '../composables/useCandidaturesFilters'
import { useCandidaturesToolbar } from '../composables/useCandidaturesToolbar'
import CandidaturesFiltersDrawer from './CandidaturesFiltersDrawer.vue'
import CandidaturesViewSwitch from './CandidaturesViewSwitch.vue'

defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const toolbar = useCandidaturesToolbar()

const route = useRoute()
const currentView = computed(() => route.meta.candidaturesView ?? 'kanban')

const filters = useCandidaturesFilters()

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
</script>

<template>
  <CspTableToolbar
    :bordered="false"
    :count="toolbar.count"
    :pending="toolbar.pending"
    :selection-count="toolbar.selectionCount"
    :selection-label="toolbar.selectionLabel"
  >
    <template #start>
      <CandidaturesViewSwitch
        :organisme-uuid="organismeUuid"
        :recrutement-uuid="recrutementUuid"
        :current="currentView"
      />
    </template>
    <template #selection-actions>
      <CspButton
        v-for="action in toolbar.selectionActions"
        :key="action.label"
        :label="action.label"
        :icon="action.icon"
        variant="secondary"
        @click="action.onClick"
      />
    </template>
    <CspSearchBar
      v-model="search"
      mode="live"
      label="Rechercher un candidat"
      hide-label
      placeholder="Rechercher un candidat…"
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
  <CandidaturesFiltersDrawer
    v-model:open="isFiltersDrawerOpen"
    v-model:etapes="filtersDraft.etapes"
    :etape-options="etapeOptions"
    :can-reset="canResetFilters"
    @apply="applyFilters"
    @reset="filters.reset"
  />
</template>
