<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { useRecrutementCandidatures } from '../composables/useRecrutementCandidatures'
import { formatRecrutementMeta } from '../format'

const router = useRouter()
const recrutementUuid = router.currentRoute.value.params.recrutementUuid as string

const {
  pending,
  error,
  candidatureListe,
  recrutementDetail,
  load,
} = useRecrutementCandidatures(TEMP_ORGANISME_UUID, recrutementUuid)

onMounted(() => {
  void load()
})

const title = computed(() => recrutementDetail.value?.intitule ?? 'Offre')

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  { label: title.value },
])

const metaItems = computed(() => recrutementDetail.value ? formatRecrutementMeta(recrutementDetail.value) : [])

const TABS: CspTabItem[] = [
  { value: 'recrutements', label: 'Recrutements' },
  { value: 'activites-et-taches', label: 'Activités et tâches' },
]
const activeTab = ref<'recrutements' | 'activites-et-taches'>('recrutements')
</script>

<template>
  <div class="recrutement-candidatures-view">
    <CspPageHeader
      :title="title"
      :breadcrumb="breadcrumb"
    />
    <CspMetaList :items="metaItems" />
    <CspTabs
      v-model="activeTab"
    >
      <CspTabsList :tabs="TABS" />
      <CspTabsPanels :tabs="TABS">
        <template #recrutements>
          <div v-if="pending">
            Chargement...
          </div>
          <div v-else-if="error">
            Erreur lors du chargement des candidatures
          </div>
          <template v-else>
            candidatures : {{ candidatureListe?.count }}
          </template>
        </template>
        <template #activites-et-taches>
          <div>Activités et tâches</div>
        </template>
      </CspTabsPanels>
    </CspTabs>
  </div>
</template>

<style scoped lang="scss">
.recrutement-candidatures-view {
  padding: 2rem;
}
</style>
