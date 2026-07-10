<script setup lang="ts">
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { CANDIDATURE_LISTE_COLUMNS } from '../columns'
import CandidaturesLayout from '../components/CandidaturesLayout.vue'
import { useCandidaturesListe } from '../composables/useCandidaturesListe'

const router = useRouter()
const recrutementUuid = router.currentRoute.value.params.recrutementUuid as string

const {
  pending,
  error,
  candidatureListe,
  recrutementDetail,
  load,
} = useCandidaturesListe(TEMP_ORGANISME_UUID, recrutementUuid)

onMounted(() => {
  void load()
})

const TABS: CspTabItem[] = [
  { value: 'recrutements', label: 'Recrutements' },
  { value: 'activites-et-taches', label: 'Activités et tâches' },
]
const activeTab = ref<'recrutements' | 'activites-et-taches'>('recrutements')

const PAGE_SIZE = 6
const candidatureListePage = ref(1)
</script>

<template>
  <CandidaturesLayout
    :recrutement-uuid="recrutementUuid"
    :recrutement-detail="recrutementDetail"
    current-view="liste"
    :pending="pending"
    :error="error"
  >
    <CspTabs v-model="activeTab">
      <CspTabsList :tabs="TABS" />
      <CspTabsPanels :tabs="TABS">
        <template #recrutements>
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
        <template #activites-et-taches>
          <div>Activités et tâches</div>
        </template>
      </CspTabsPanels>
    </CspTabs>
  </CandidaturesLayout>
</template>
