<script setup lang="ts">
import { useQuery } from '@pinia/colada'
import { computed, ref, useTemplateRef } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { pluralize } from '@/utils/format'
import { CANDIDATURE_LISTE_COLUMNS } from '../columns'
import CandidaturesToolbar from '../components/CandidaturesToolbar.vue'
import { useCandidatureLinkFocus } from '../composables/useCandidatureLinkFocus'
import { provideCandidatureSequence } from '../composables/useCandidatureNavigation'
import { useCandidaturesFilters } from '../composables/useCandidaturesFilters'
import { candidatureListeQuery } from '../queries'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid?: string
}>()
const liste = useQuery(() => candidatureListeQuery(props))
const filters = useCandidaturesFilters()
const filteredCandidatures = computed(() => filters.filterCandidatures(liste.data.value?.results ?? []))
const { listeSort } = filters

const showSkeleton = useMinimumPending(liste.isPending)

const table = useTemplateRef('table')
provideCandidatureSequence(() => table.value?.sortedRowIds ?? [])
useCandidatureLinkFocus()

const candidatureListePage = ref(1)

const countLabel = computed(() => {
  const count = filteredCandidatures.value.length
  return `${count} ${pluralize(count, 'candidature')}`
})
</script>

<template>
  <CandidaturesToolbar
    :organisme-uuid="organismeUuid"
    :recrutement-uuid="recrutementUuid"
    :error="Boolean(liste.error.value)"
    :count="countLabel"
    :pending="showSkeleton"
  />
  <CspAsyncSection
    :pending="showSkeleton"
    :error="liste.error.value"
    loading-label="Chargement des candidatures"
    error-title="Une erreur est survenue lors du chargement des candidatures."
  >
    <template #skeleton>
      <CspSkeletonTable
        :rows="TABLE_PAGE_SIZE"
        :columns="CANDIDATURE_LISTE_COLUMNS.length"
        with-footer
      />
    </template>

    <CspDataTable
      ref="table"
      v-model:sort="listeSort"
      v-model:page="candidatureListePage"
      :rows="filteredCandidatures"
      :columns="CANDIDATURE_LISTE_COLUMNS"
      :row-key="row => row.uuid"
      :current-id="props.candidatureUuid"
      caption="Candidatures"
      empty-label="Aucune candidature"
      :page-size="TABLE_PAGE_SIZE"
    />
  </CspAsyncSection>

  <router-view />
</template>
