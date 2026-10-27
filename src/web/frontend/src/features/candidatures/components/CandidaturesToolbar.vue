<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { useCandidaturesFilters } from '../composables/useCandidaturesFilters'
import CandidaturesFiltersDrawer from './CandidaturesFiltersDrawer.vue'
import CandidaturesViewSwitch from './CandidaturesViewSwitch.vue'

withDefaults(defineProps<{
  organismeUuid: string
  recrutementUuid: string
  count: string
  error?: boolean
  pending?: boolean
  selectionCount?: number
  selectionLabel?: string
}>(), {
  error: false,
  pending: false,
  selectionCount: 0,
  selectionLabel: undefined,
})

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
  <CandidaturesViewSwitch
    v-if="error"
    :organisme-uuid="organismeUuid"
    :recrutement-uuid="recrutementUuid"
    :current="currentView"
  />
  <CspTableToolbar
    v-else
    :bordered="false"
    :count="count"
    :pending="pending"
    :selection-count="selectionCount"
    :selection-label="selectionLabel"
  >
    <template #start>
      <CandidaturesViewSwitch
        :organisme-uuid="organismeUuid"
        :recrutement-uuid="recrutementUuid"
        :current="currentView"
      />
    </template>
    <template #selection-actions>
      <slot name="selection-actions" />
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
