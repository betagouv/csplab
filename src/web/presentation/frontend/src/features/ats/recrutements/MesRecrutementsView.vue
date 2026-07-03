<script setup lang="ts">
import type {
  RecrutementKey,
} from './types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { onMounted, ref, watch } from 'vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import AtsAppShell from '../components/AtsAppShell.vue'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from './columns'
import { useRecrutements } from './useRecrutements'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements' },
]

const activeTab = ref<RecrutementKey>('actifs')

const TABS: CspTabItem[] = [
  { value: 'actifs', label: 'Recrutements en cours' },
  { value: 'archives', label: 'Offres archivées' },
]
const {
  state: recrutementsState,
  data: recrutementsData,
  load: loadRecrutements,
  has: hasRecrutements,
} = useRecrutements({ source: 'mock' })

onMounted(() => {
  watch(activeTab, (newTab) => {
    if (!hasRecrutements(newTab)) {
      void loadRecrutements(newTab)
    }
  }, { immediate: true })
})

function openOffre(offreUuid: string) {
  // eslint-disable-next-line no-console
  console.log('openOffre', offreUuid)
}

const recrutementsActifsPage = ref(1)
const recrutementsArchivesPage = ref(1)

const PAGE_SIZE = 6
</script>

<template>
  <AtsAppShell>
    <div class="mes-recrutement-view">
      <CspPageHeader
        title="Mes recrutements"
        :breadcrumb="BREADCRUMB"
        class="mes-recrutement-view__header"
      />
      <CspTabs
        v-model="activeTab"
      >
        <CspTabsList :tabs="TABS" />
        <div
          v-if="(
            recrutementsState === 'idle'
            || recrutementsState === 'loading'
          )"
          class="mes-recrutement-view__loading"
        >
          Chargement des recrutements...
        </div>
        <div
          v-else-if="recrutementsState === 'error'"
          class="mes-recrutement-view__error"
        >
          Une erreur est survenue lors du chargement des recrutements.
        </div>
        <CspTabsPanels
          v-else
          :tabs="TABS"
        >
          <template #actifs>
            <p class="mes-recrutement-view__count">
              {{ recrutementsData.actifs.length }} recrutement{{ recrutementsData.actifs.length > 1 ? 's' : '' }} en cours
            </p>
            <CspDataTable
              v-model:page="recrutementsActifsPage"
              :rows="recrutementsData.actifs"
              :columns="RECRUTEMENTS_ACTIFS_COLUMNS"
              :row-key="row => row.offer_id"
              activation-mode="cell"
              caption="Recrutements en cours"
              empty-label="Aucun recrutement en cours"
              :page-size="PAGE_SIZE"
              @activate="openOffre"
            >
              <template #header-candidatures="{ label }">
                <div class="mes-recrutement-view__candidatures-head">
                  <span>{{ label }}</span>
                  <span class="mes-recrutement-view__candidatures-legend">
                    # • À traiter • En cours
                  </span>
                </div>
              </template>
            </CspDataTable>
          </template>

          <template #archives>
            <p class="mes-recrutement-view__count">
              {{ recrutementsData.archives.length }} offre{{ recrutementsData.archives.length > 1 ? 's' : '' }} archivée{{ recrutementsData.archives.length > 1 ? 's' : '' }}
            </p>
            <CspDataTable
              v-model:page="recrutementsArchivesPage"
              :rows="recrutementsData.archives"
              :columns="RECRUTEMENTS_ARCHIVES_COLUMNS"
              :row-key="row => row.offer_id"
              activation-mode="cell"
              caption="Offres archivées"
              empty-label="Aucune offre archivée"
              :page-size="PAGE_SIZE"
              @activate="openOffre"
            />
          </template>
        </CspTabsPanels>
      </CspTabs>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.mes-recrutement-view {
  padding: 2rem;
}

.mes-recrutement-view__idle,
.mes-recrutement-view__loading,
.mes-recrutement-view__error {
  padding: 1rem 0;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__error {
  color: var(--text-default-error);
}

.mes-recrutement-view__count {
  margin: 0 0 1rem;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__candidatures-head {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.mes-recrutement-view__candidatures-legend {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
