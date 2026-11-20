<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { CANDIDATURES_VIEW_ROUTE_NAMES } from '@/router/names'
import { pluralize } from '@/utils/format'
import { RECRUTEMENTS_ARCHIVES_COLUMNS } from '../columns'
import RecrutementsArchivesFiltersDrawer from '../components/RecrutementsArchivesFiltersDrawer.vue'
import { useRecrutements } from '../composables/useRecrutements'
import { useRecrutementsFilters } from '../composables/useRecrutementsFilters'

const props = defineProps<{
  organismeUuid: string
}>()

const router = useRouter()

const { pendingArchives, data: recrutementsData } = useRecrutements(() => props.organismeUuid, 'archives')

const showArchivesSkeleton = useMinimumPending(pendingArchives, 300)

function openOffre(recrutementUuid: string) {
  void router.push({
    name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
    params: { organismeUuid: props.organismeUuid, recrutementUuid },
  })
}

const recrutementsArchivesPage = ref(1)

const archivesFilters = useRecrutementsFilters(computed(() => recrutementsData.archives))

const archivesFiltersDrawer = useDisclosure()

function openArchivesFilters() {
  archivesFilters.syncDraft()
  archivesFiltersDrawer.open()
}

function applyArchivesFilters() {
  archivesFilters.apply()
  archivesFiltersDrawer.close()
}

const aucuneOffreArchivee = computed(
  () => !showArchivesSkeleton.value && recrutementsData.archives.length === 0,
)

const archivesCountLabel = computed(() => {
  const count = archivesFilters.filtered.value.length
  return `${count} ${pluralize(count, 'recrutement terminé', 'recrutements terminés')}`
})
</script>

<template>
  <CspEmptyState
    v-if="aucuneOffreArchivee"
    icon="ri:archive-line"
    title="Aucun recrutement terminé"
  />
  <template v-else>
    <CspTableToolbar
      :bordered="false"
      :count="archivesCountLabel"
      :pending="showArchivesSkeleton"
    >
      <CspSearchBar
        v-model="archivesFilters.search.value"
        mode="live"
        label="Rechercher un recrutement"
        hide-label
        placeholder="Intitulé, référence, responsable…"
      />
      <CspButton
        :label="archivesFilters.activeFiltersCount.value ? `Filtres (${archivesFilters.activeFiltersCount.value})` : 'Filtres'"
        variant="tertiary"
        icon="ri:filter-line"
        is-icon-left
        @click="openArchivesFilters"
      />
    </CspTableToolbar>
    <RecrutementsArchivesFiltersDrawer
      v-model:open="archivesFiltersDrawer.isOpen.value"
      v-model:responsable="archivesFilters.draft.responsable"
      v-model:nature-offre="archivesFilters.draft.natureOffre"
      :responsable-options="archivesFilters.responsableOptions.value"
      :can-reset="archivesFilters.canReset.value"
      @apply="applyArchivesFilters"
      @reset="archivesFilters.reset()"
    />
    <CspAsyncSection
      :pending="showArchivesSkeleton"
      loading-label="Chargement des recrutements terminés"
    >
      <template #skeleton>
        <CspSkeletonTable
          :columns="RECRUTEMENTS_ARCHIVES_COLUMNS.length"
        />
      </template>
      <CspDataTable
        v-model:page="recrutementsArchivesPage"
        :rows="archivesFilters.filtered.value"
        :columns="RECRUTEMENTS_ARCHIVES_COLUMNS"
        :row-key="row => row.uuid"
        activation-mode="cell"
        caption="Recrutements terminés"
        empty-label="Aucun recrutement terminé"
        :page-size="TABLE_PAGE_SIZE"
        @activate="openOffre"
      />
    </CspAsyncSection>
  </template>
</template>
