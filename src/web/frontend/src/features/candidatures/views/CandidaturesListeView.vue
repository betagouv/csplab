<script setup lang="ts">
import { computed, ref, useTemplateRef } from 'vue'
import { useRoute } from 'vue-router'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { pluralize } from '@/utils/format'
import { CANDIDATURE_LISTE_COLUMNS } from '../columns'
import { useCandidatureLinkFocus } from '../composables/useCandidatureLinkFocus'
import { provideCandidatureSequence } from '../composables/useCandidatureNavigation'
import { useCandidatures } from '../composables/useCandidatures'

const { pendingListe, filters } = useCandidatures()
const { filteredCandidatures } = filters

const showSkeleton = useMinimumPending(pendingListe)

const route = useRoute()
const openCandidatureUuid = computed(() => route.params.candidatureUuid as string | undefined)

const table = useTemplateRef('table')
provideCandidatureSequence(() => table.value?.sortedRowIds ?? [])
useCandidatureLinkFocus()

const PAGE_SIZE = 6
const candidatureListePage = ref(1)

const countLabel = computed(() => {
  const count = filteredCandidatures.value.length
  return `${count} ${pluralize(count, 'candidature')}`
})
</script>

<template>
  <div
    v-if="showSkeleton"
    class="candidatures-liste-content"
    role="status"
    aria-label="Chargement des candidatures"
  >
    <p class="candidatures-liste-content__count">
      <CspSkeleton
        width="8rem"
        variant="text"
      />
    </p>
    <CspSkeletonTable
      :rows="PAGE_SIZE"
      :columns="CANDIDATURE_LISTE_COLUMNS.length"
      with-footer
    />
  </div>

  <div
    v-else
    class="candidatures-liste-content"
  >
    <p class="candidatures-liste-content__count">
      {{ countLabel }}
    </p>
    <CspDataTable
      ref="table"
      v-model:page="candidatureListePage"
      :rows="filteredCandidatures"
      :columns="CANDIDATURE_LISTE_COLUMNS"
      :row-key="row => row.uuid"
      :current-id="openCandidatureUuid"
      caption="Candidatures"
      empty-label="Aucune candidature"
      :page-size="PAGE_SIZE"
    />
  </div>

  <router-view />
</template>

<style scoped lang="scss">
.candidatures-liste-content__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}
</style>
