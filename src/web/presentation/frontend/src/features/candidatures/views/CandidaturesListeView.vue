<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { CANDIDATURE_LISTE_COLUMNS } from '../columns'
import { useCandidatures } from '../composables/useCandidatures'

const { filters } = useCandidatures()
const { filteredCandidatures } = filters

const PAGE_SIZE = 6
const candidatureListePage = ref(1)

watch(filteredCandidatures, () => {
  candidatureListePage.value = 1
})

const countLabel = computed(() => {
  const count = filteredCandidatures.value.length
  return `${count} candidature${count > 1 ? 's' : ''}`
})
</script>

<template>
  <div class="candidatures-liste-content">
    <p class="candidatures-liste-content__count">
      {{ countLabel }}
    </p>
    <CspDataTable
      v-model:page="candidatureListePage"
      :rows="filteredCandidatures"
      :columns="CANDIDATURE_LISTE_COLUMNS"
      :row-key="row => row.uuid"
      activation-mode="cell"
      caption="Candidatures"
      empty-label="Aucune candidature"
      :page-size="PAGE_SIZE"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-liste-content__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}
</style>
