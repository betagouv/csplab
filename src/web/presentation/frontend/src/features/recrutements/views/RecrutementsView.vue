<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from '../columns'
import RecrutementsActifsFiltersDrawer from '../components/RecrutementsActifsFiltersDrawer.vue'
import RecrutementsArchivesFiltersDrawer from '../components/RecrutementsArchivesFiltersDrawer.vue'

import { useRecrutements } from '../composables/useRecrutements'
import { useRecrutementsFilters } from '../composables/useRecrutementsFilters'
import { RECRUTEMENT_TAB_ICONS, RECRUTEMENT_TAB_LABELS } from '../constants/recrutement'
import { DEFAULT_RECRUTEMENT_TAB, RECRUTEMENTS_TAB_ROUTE_NAMES } from '../routes'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Recrutements' },
]

const route = useRoute()
const router = useRouter()
const organismeUuid = computed(() => route.params.organismeUuid as string)

const activeTab = useRouteTab(RECRUTEMENTS_TAB_ROUTE_NAMES, DEFAULT_RECRUTEMENT_TAB)

const TABS = tabItems(RECRUTEMENT_TAB_LABELS, RECRUTEMENT_TAB_ICONS)

const {
  pendingActifs,
  pendingArchives,
  error: recrutementsError,
  data: recrutementsData,
} = useRecrutements(organismeUuid, activeTab)

const showActifsSkeleton = useMinimumPending(pendingActifs, 300)
const showArchivesSkeleton = useMinimumPending(pendingArchives, 300)

function openOffre(recrutementUuid: string) {
  void router.push({
    name: 'recrutement-candidatures-kanban',
    params: { organismeUuid: organismeUuid.value, recrutementUuid },
  })
}

const recrutementsActifsPage = ref(1)
const recrutementsArchivesPage = ref(1)

const PAGE_SIZE = 6

const actifsFilters = useRecrutementsFilters(computed(() => recrutementsData.actifs))
const archivesFilters = useRecrutementsFilters(computed(() => recrutementsData.archives))

const actifsFiltersDrawer = useDisclosure()
const archivesFiltersDrawer = useDisclosure()

function openActifsFilters() {
  actifsFilters.syncDraft()
  actifsFiltersDrawer.open()
}

function applyActifsFilters() {
  actifsFilters.apply()
  actifsFiltersDrawer.close()
}

function openArchivesFilters() {
  archivesFilters.syncDraft()
  archivesFiltersDrawer.open()
}

function applyArchivesFilters() {
  archivesFilters.apply()
  archivesFiltersDrawer.close()
}

watch(actifsFilters.filtered, () => {
  recrutementsActifsPage.value = 1
})

watch(archivesFilters.filtered, () => {
  recrutementsArchivesPage.value = 1
})

const actifsCountLabel = computed(() => {
  const count = actifsFilters.filtered.value.length
  return `${count} recrutement${count > 1 ? 's' : ''} en cours`
})

const archivesCountLabel = computed(() => {
  const count = archivesFilters.filtered.value.length
  return `${count} offre${count > 1 ? 's' : ''} archivée${count > 1 ? 's' : ''}`
})
</script>

<template>
  <CspPageHeader
    title="Recrutements"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <p class="mes-recrutement-view__subtitle">
        Retrouvez ici l’ensemble des recrutements en cours et archivés.
      </p>
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    class="mes-recrutement-view"
    :tabs="TABS"
  >
    <template
      v-if="recrutementsError"
      #shared
    >
      <CspErrorState
        title="Une erreur est survenue lors du chargement des recrutements."
      />
    </template>
    <template
      v-if="!recrutementsError"
      #tab-actifs
    >
      <CspTableToolbar :bordered="false">
        <template #status>
          <CspSkeleton
            v-if="showActifsSkeleton"
            width="12rem"
            height="0.9375rem"
          />
          <p
            v-else
            class="mes-recrutement-view__count"
          >
            {{ actifsCountLabel }}
          </p>
        </template>
        <CspInput
          v-model="actifsFilters.search.value"
          type="search"
          aria-label="Rechercher un recrutement"
          placeholder="Rechercher une offre, une référence,…"
          class="mes-recrutement-view__search"
        />
        <CspButton
          :label="actifsFilters.activeFiltersCount.value ? `Filtres (${actifsFilters.activeFiltersCount.value})` : 'Filtres'"
          variant="tertiary"
          icon="ri:filter-line"
          is-icon-left
          @click="openActifsFilters"
        />
      </CspTableToolbar>
      <RecrutementsActifsFiltersDrawer
        v-model:open="actifsFiltersDrawer.isOpen.value"
        v-model:responsable="actifsFilters.draft.responsable"
        :responsable-options="actifsFilters.responsableOptions.value"
        :can-reset="actifsFilters.canReset.value"
        @apply="applyActifsFilters"
        @reset="actifsFilters.reset()"
      />
      <CspAsyncSection
        :pending="showActifsSkeleton"
        loading-label="Chargement des recrutements en cours"
      >
        <template #skeleton>
          <CspSkeletonTable
            :rows="PAGE_SIZE"
            :columns="6"
            with-footer
          />
        </template>
        <CspDataTable
          v-model:page="recrutementsActifsPage"
          :rows="actifsFilters.filtered.value"
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
                # · À traiter · En cours
              </span>
            </div>
          </template>
        </CspDataTable>
      </CspAsyncSection>
    </template>
    <template
      v-if="!recrutementsError"
      #tab-archives
    >
      <CspTableToolbar :bordered="false">
        <template #status>
          <CspSkeleton
            v-if="showArchivesSkeleton"
            width="12rem"
            height="0.9375rem"
          />
          <p
            v-else
            class="mes-recrutement-view__count"
          >
            {{ archivesCountLabel }}
          </p>
        </template>
        <CspInput
          v-model="archivesFilters.search.value"
          type="search"
          aria-label="Rechercher un recrutement"
          placeholder="Rechercher une offre, une référence,…"
          class="mes-recrutement-view__search"
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
        v-model:type-contrat="archivesFilters.draft.typeContrat"
        :responsable-options="archivesFilters.responsableOptions.value"
        :can-reset="archivesFilters.canReset.value"
        @apply="applyArchivesFilters"
        @reset="archivesFilters.reset()"
      />
      <CspAsyncSection
        :pending="showArchivesSkeleton"
        loading-label="Chargement des offres archivées"
      >
        <template #skeleton>
          <CspSkeletonTable
            :rows="PAGE_SIZE"
            :columns="6"
            with-footer
          />
        </template>
        <CspDataTable
          v-model:page="recrutementsArchivesPage"
          :rows="archivesFilters.filtered.value"
          :columns="RECRUTEMENTS_ARCHIVES_COLUMNS"
          :row-key="row => row.offer_id"
          activation-mode="cell"
          caption="Offres archivées"
          empty-label="Aucune offre archivée"
          :page-size="PAGE_SIZE"
          @activate="openOffre"
        />
      </CspAsyncSection>
    </template>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.mes-recrutement-view__subtitle {
  margin: 0;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.mes-recrutement-view__search {
  min-width: 20rem;
}

.mes-recrutement-view__candidatures-head {
  display: flex;
  flex-direction: column;
  max-height: 1rem;
  & > span:first-child {
    margin-top: -0.75rem;
  }
}

.mes-recrutement-view__candidatures-legend {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
