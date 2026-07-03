<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { onMounted, ref, watch } from 'vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import AtsAppShell from '../components/AtsAppShell.vue'
import { useRecrutements } from './useRecrutements'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements' },
]

const activeTab = ref<'actifs' | 'archives'>('actifs')

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
          v-if="recrutementsState === 'idle'"
          class="mes-recrutement-view__idle"
        >
          Aucun recrutement à afficher.
        </div>
        <div
          v-else-if="recrutementsState === 'loading'"
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
            recrutements en cours : {{ recrutementsData.actifs.length }}
          </template>

          <template #archives>
            recrutements archivés : {{ recrutementsData.archives.length }}
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
</style>
