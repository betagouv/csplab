<script setup lang="ts">
import { ref } from 'vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { CANDIDATURE_LISTE_COLUMNS } from '../columns'
import { useCandidatures } from '../composables/useCandidatures'

const { candidatureListe } = useCandidatures()

const PAGE_SIZE = 6
const candidatureListePage = ref(1)
</script>

<template>
  <CspDataTable
    v-model:page="candidatureListePage"
    :rows="candidatureListe?.results ?? []"
    :columns="CANDIDATURE_LISTE_COLUMNS"
    :row-key="row => row.uuid"
    activation-mode="cell"
    caption="Candidatures"
    empty-label="Aucune candidature"
    :page-size="PAGE_SIZE"
  />
</template>
