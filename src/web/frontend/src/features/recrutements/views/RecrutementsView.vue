<script setup lang="ts">
import type { AssignationResponsableResultat, RecrutementKey } from '../types'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { ToastOptions } from '@/composables/ui/useToast'
import type { AgentRecherche } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { HttpError, isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTableSelection } from '@/composables/data/useTableSelection'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import { useToast } from '@/composables/ui/useToast'
import { formatAgentName } from '@/features/organismes/format'
import { CANDIDATURES_VIEW_ROUTE_NAMES, HOME_ROUTE_NAME, RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { pluralize } from '@/utils/format'
import ForbiddenView from '@/views/ForbiddenView.vue'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from '../columns'
import AssignationResponsableDrawer from '../components/AssignationResponsableDrawer.vue'
import RecrutementsActifsFiltersDrawer from '../components/RecrutementsActifsFiltersDrawer.vue'
import RecrutementsArchivesFiltersDrawer from '../components/RecrutementsArchivesFiltersDrawer.vue'
import { useAssignationResponsable } from '../composables/useAssignationResponsable'
import { useRecrutements } from '../composables/useRecrutements'
import { useRecrutementsFilters } from '../composables/useRecrutementsFilters'
import { RECRUTEMENT_TAB_ICONS, RECRUTEMENT_TAB_LABELS } from '../constants/recrutement'

const props = defineProps<{
  organismeUuid: string
}>()

const AUCUN_RECRUTEMENT_EN_COURS_DESCRIPTION = 'Les recrutements auxquels vous participez apparaissent ici. Pour accéder à un recrutement, contactez la personne responsable dans votre organisation.'

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: { name: HOME_ROUTE_NAME } },
  { label: 'Recrutements' },
]

const router = useRouter()

const activeTab = useRouteTab<RecrutementKey>(RECRUTEMENTS_TAB_ROUTE_NAMES, 'actifs')

const TABS = tabItems(RECRUTEMENT_TAB_LABELS, RECRUTEMENT_TAB_ICONS)

const {
  pendingActifs,
  pendingArchives,
  error: recrutementsError,
  data: recrutementsData,
} = useRecrutements(() => props.organismeUuid, activeTab)

const forbidden = computed(() => isHttpStatus(recrutementsError.value, 403))

const showActifsSkeleton = useMinimumPending(pendingActifs, 300)
const showArchivesSkeleton = useMinimumPending(pendingArchives, 300)

function openOffre(recrutementUuid: string) {
  void router.push({
    name: CANDIDATURES_VIEW_ROUTE_NAMES.kanban,
    params: { organismeUuid: props.organismeUuid, recrutementUuid },
  })
}

const recrutementsActifsPage = ref(1)
const recrutementsArchivesPage = ref(1)

const PAGE_SIZE = 6

const actifsFilters = useRecrutementsFilters(computed(() => recrutementsData.actifs))
const archivesFilters = useRecrutementsFilters(computed(() => recrutementsData.archives))

const actifsFiltersDrawer = useDisclosure()
const archivesFiltersDrawer = useDisclosure()

const { canManageOrganisme } = useRouteOrganisme()
const { addToast } = useToast()

const selection = useTableSelection(actifsFilters.filtered, row => row.uuid)
const assignationDrawer = useDisclosure()
const {
  status: responsableStatus,
  foundAgent,
  searching,
  search: searchResponsable,
  assign,
  submitting,
  reset: resetResponsable,
} = useAssignationResponsable(() => props.organismeUuid)

const selectionLabel = computed(() => {
  const count = selection.count.value
  return `${count} ${pluralize(count, 'offre sélectionnée', 'offres sélectionnées')}`
})

function assignationToast(
  resultat: AssignationResponsableResultat,
  agent: AgentRecherche | null,
): ToastOptions {
  const nom = agent ? formatAgentName(agent) || agent.email : 'Le membre choisi'
  const reussites = resultat.reussites.length
  const assignees = `${nom} est responsable de ${reussites} ${pluralize(reussites, 'offre')}`

  if (resultat.echecs.length === 0) {
    return {
      variant: 'success',
      title: 'Responsable assigné',
      description: `${assignees}.`,
    }
  }
  const echecs = resultat.echecs.length
  return {
    variant: 'warning',
    title: 'Assignation partielle',
    description: `${assignees}, ${echecs} ${pluralize(echecs, 'offre ignorée', 'offres ignorées')}.`,
  }
}

function assignationErrorTitle(assignationError: unknown): string {
  if (assignationError instanceof HttpError && assignationError.status === 403) {
    return 'Vous n\'avez pas les droits pour assigner un responsable'
  }
  if (assignationError instanceof HttpError && assignationError.status === 404) {
    return 'Ce membre n\'est plus rattaché à l\'organisme'
  }
  return 'L\'assignation du responsable a échoué'
}

async function handleSearchResponsable(email: string) {
  try {
    await searchResponsable(email)
  }
  catch {
    addToast({ variant: 'error', title: 'La recherche a échoué' })
  }
}

async function handleAssign() {
  const recrutementIds = selection.selected.value.map(row => row.uuid)

  try {
    const resultat = await assign(recrutementIds)
    const agent = foundAgent.value
    assignationDrawer.close()
    selection.clear()
    addToast(assignationToast(resultat, agent))
  }
  catch (assignationError) {
    addToast({ variant: 'error', title: assignationErrorTitle(assignationError) })
  }
}

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

const aucunRecrutementActif = computed(
  () => !showActifsSkeleton.value && recrutementsData.actifs.length === 0,
)

const aucuneOffreArchivee = computed(
  () => !showArchivesSkeleton.value && recrutementsData.archives.length === 0,
)

const actifsCountLabel = computed(() => {
  const count = actifsFilters.filtered.value.length
  return `${count} recrutement${count > 1 ? 's' : ''} en cours`
})

const archivesCountLabel = computed(() => {
  const count = archivesFilters.filtered.value.length
  return `${count} recrutement${count > 1 ? 's' : ''} terminé${count > 1 ? 's' : ''}`
})
</script>

<template>
  <ForbiddenView v-if="forbidden" />
  <template v-else>
    <CspPageHeader
      title="Recrutements"
      subtitle="Retrouvez ici l’ensemble des recrutements en cours et archivés."
      :breadcrumb="BREADCRUMB"
    >
      <template #subtitle>
        <p class="mes-recrutement-view__subtitle">
          Retrouvez ici l’ensemble des recrutements en cours et terminés.
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
        <CspEmptyState
          v-if="aucunRecrutementActif"
          icon="ri:briefcase-line"
          title="Vous n’avez pas de recrutement en cours"
          :description="AUCUN_RECRUTEMENT_EN_COURS_DESCRIPTION"
        />
        <template v-else>
          <CspTableToolbar
            :bordered="false"
            :selection-count="selection.count.value"
            :selection-label="selectionLabel"
          >
            <template #selection-actions>
              <CspButton
                label="Assigner un responsable"
                @click="assignationDrawer.open()"
              />
            </template>
            <template #status>
              <p class="mes-recrutement-view__count">
                <CspSkeleton
                  v-if="showActifsSkeleton"
                  width="12rem"
                  variant="text"
                />
                <template v-else>
                  {{ actifsCountLabel }}
                </template>
              </p>
            </template>
            <CspSearchBar
              v-model="actifsFilters.search.value"
              mode="live"
              label="Rechercher un recrutement"
              hide-label
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
          <AssignationResponsableDrawer
            v-model:open="assignationDrawer.isOpen.value"
            :recrutements="selection.selected.value"
            :status="responsableStatus"
            :agent="foundAgent"
            :searching="searching"
            :submitting="submitting"
            @remove="selection.toggle"
            @search="handleSearchResponsable"
            @assign="handleAssign"
            @reset="resetResponsable"
          />
          <CspAsyncSection
            :pending="showActifsSkeleton"
            loading-label="Chargement des recrutements en cours"
          >
            <template #skeleton>
              <CspSkeletonTable
                :rows="PAGE_SIZE"
                :columns="canManageOrganisme ? 7 : 6"
                with-footer
              />
            </template>
            <CspDataTable
              v-model:page="recrutementsActifsPage"
              :rows="actifsFilters.filtered.value"
              :columns="RECRUTEMENTS_ACTIFS_COLUMNS"
              :row-key="row => row.uuid"
              :selection-mode="canManageOrganisme ? 'checkbox' : 'none'"
              :selected-ids="selection.selectedIds.value"
              :selection-label="row => `Sélectionner ${row.intitule}`"
              activation-mode="cell"
              caption="Recrutements en cours"
              empty-label="Aucun recrutement en cours"
              :page-size="PAGE_SIZE"
              @activate="openOffre"
              @toggle-row="selection.toggle"
              @toggle-all="selection.toggleVisible"
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
      </template>
      <template
        v-if="!recrutementsError"
        #tab-archives
      >
        <CspEmptyState
          v-if="aucuneOffreArchivee"
          icon="ri:archive-line"
          title="Aucun recrutement terminé"
        />
        <template v-else>
          <CspTableToolbar :bordered="false">
            <template #status>
              <p class="mes-recrutement-view__count">
                <CspSkeleton
                  v-if="showArchivesSkeleton"
                  width="12rem"
                  variant="text"
                />
                <template v-else>
                  {{ archivesCountLabel }}
                </template>
              </p>
            </template>
            <CspSearchBar
              v-model="archivesFilters.search.value"
              mode="live"
              label="Rechercher un recrutement"
              hide-label
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
                :rows="PAGE_SIZE"
                :columns="6"
                with-footer
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
              :page-size="PAGE_SIZE"
              @activate="openOffre"
            />
          </CspAsyncSection>
        </template>
      </template>
    </CspPageContainer>
  </template>
</template>

<style scoped lang="scss">
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
