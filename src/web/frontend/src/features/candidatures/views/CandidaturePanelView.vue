<script setup lang="ts">
import type { CandidaturePanelTabKey } from '../constants/candidature'
import type { CandidaturesViewName } from '@/router/names'
import { useQueryCache } from '@pinia/colada'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import CspSequenceNav from '@/components/base/CspSequenceNav/CspSequenceNav.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import CspUnsavedChangesDialog from '@/components/base/CspUnsavedChangesDialog/CspUnsavedChangesDialog.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { tabItems } from '@/composables/navigation/tabs'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { useUnsavedChangesGuard } from '@/composables/navigation/useUnsavedChanges'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'
import MessagesSection from '@/features/messages/components/MessagesSection.vue'
import { formatElapsedDays } from '@/utils/date'
import CandidatureActivites from '../components/CandidatureActivites.vue'
import CandidatureCv from '../components/CandidatureCv.vue'
import CandidatureDocuments from '../components/CandidatureDocuments.vue'
import CandidatureHistorique from '../components/CandidatureHistorique.vue'
import CandidatureNoteForm from '../components/CandidatureNoteForm.vue'
import CandidatureNotes from '../components/CandidatureNotes.vue'
import ChangerEtapePopover from '../components/ChangerEtapePopover.vue'
import RefusCandidatureDialog from '../components/RefusCandidatureDialog.vue'
import { useCandidatureDetail } from '../composables/useCandidatureDetail'
import { useCandidatureNavigation } from '../composables/useCandidatureNavigation'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'
import { useEtapeChange } from '../composables/useEtapeChange'
import { CANDIDATURE_PANEL_TAB_ICONS, CANDIDATURE_PANEL_TAB_LABELS } from '../constants/candidature'
import { candidatureDetailQuery } from '../queries'
import { formatCandidatNom } from '../utils/candidat'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}>()

const router = useRouter()

function paramsFor(uuid: string) {
  return { organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid, candidatureUuid: uuid }
}
const candidatureParams = computed(() => paramsFor(props.candidatureUuid))
const { candidature, pending, error, notFound } = useCandidatureDetail(() => candidatureParams.value)

const showSkeleton = useMinimumPending(pending)
const loadFailed = computed(() => Boolean(error.value) && !notFound.value)

const title = computed(() => candidature.value ? formatCandidatNom(candidature.value.candidat) : 'Candidature')
const description = computed(() =>
  candidature.value ? `Candidature ${formatElapsedDays(candidature.value.date_candidature)}` : null,
)

const etape = computed(() => candidature.value?.etape_actuelle ?? null)
const navigation = useCandidatureNavigation(() => props.candidatureUuid)
const { position, goPrevious, goNext } = navigation

const queryCache = useQueryCache()
watch(position, (current) => {
  for (const uuid of [current?.previousUuid, current?.nextUuid]) {
    if (uuid) {
      void queryCache.refresh(queryCache.ensure(candidatureDetailQuery(paramsFor(uuid))))
    }
  }
}, { immediate: true })

const scrollArea = ref<HTMLElement | null>(null)
watch(() => props.candidatureUuid, () => {
  if (scrollArea.value) {
    scrollArea.value.scrollTop = 0
  }
})

const TABS = tabItems(CANDIDATURE_PANEL_TAB_LABELS, CANDIDATURE_PANEL_TAB_ICONS)
const { view, names: panelRouteNames, parentName } = useCandidaturePanelRoutes()
const SEQUENCE_LABELS = {
  kanban: 'Navigation entre les candidatures de l\'étape',
  liste: 'Navigation entre les candidatures de la liste',
} as const satisfies Record<CandidaturesViewName, string>
const activeTab = useRouteTab<CandidaturePanelTabKey>(() => panelRouteNames.value.tabs, 'candidature')

useDocumentTitle(
  () => CANDIDATURE_PANEL_TAB_LABELS[activeTab.value],
  () => candidature.value && formatCandidatNom(candidature.value.candidat),
)
const TABS_WITHOUT_ASIDE: CandidaturePanelTabKey[] = ['historique', 'messages']
const isMessagesTab = computed(() => activeTab.value === 'messages')
const showAside = computed(() => !TABS_WITHOUT_ASIDE.includes(activeTab.value))

function close(): void {
  void router.push({ name: parentName.value })
}

const unsavedChanges = useUnsavedChangesGuard({
  ignore: to => to.params.candidatureUuid === props.candidatureUuid,
})

function leaveMovedCandidature(): void {
  if (position.value?.nextUuid) {
    navigation.navigateTo(position.value.nextUuid)
  }
  else {
    close()
  }
}

const etapeChange = useEtapeChange(candidature, leaveMovedCandidature)

async function requestEtapeChange(targetEtapeUuid: string): Promise<void> {
  if (await unsavedChanges.confirmLeave()) {
    etapeChange.request(targetEtapeUuid)
  }
}

function handleUpdateOpen(open: boolean): void {
  if (!open) {
    close()
  }
}
</script>

<template>
  <CspDrawer
    :open="true"
    :overlay="false"
    aria-label="Candidature"
    close-label="Fermer la candidature"
    class="candidature-panel"
    @update:open="handleUpdateOpen"
  >
    <template
      v-if="candidature && etape"
      #end
    >
      <ChangerEtapePopover
        :etapes="etapeChange.etapes.value"
        :current-etape-uuid="etape.uuid"
        @confirm="requestEtapeChange"
      />
    </template>

    <template #title>
      <CspSkeleton
        v-if="showSkeleton"
        width="12rem"
        variant="text"
      />
      <template v-else>
        {{ title }}
      </template>
    </template>

    <template
      v-if="showSkeleton || description"
      #description
    >
      <CspSkeleton
        v-if="showSkeleton"
        width="9rem"
        variant="text"
      />
      <template v-else>
        {{ description }}
      </template>
    </template>

    <div
      v-if="loadFailed || notFound"
      class="candidature-panel__exception"
    >
      <CspErrorState
        v-if="loadFailed"
        title="Une erreur est survenue lors du chargement de la candidature."
      />
      <CspEmptyState
        v-else
        icon="ri:search-line"
        title="Cette candidature n'est pas accessible."
        description="Elle n'existe pas ou ne vous est pas accessible. Contactez le superviseur de votre organisme si besoin."
      />
    </div>

    <div
      v-else
      class="candidature-panel__body"
    >
      <CspTabs
        v-model="activeTab"
        fill
        class="candidature-panel__tabs"
      >
        <CspTabsList :tabs="TABS" />
        <div
          ref="scrollArea"
          class="candidature-panel__scroll"
          :class="{ 'candidature-panel__scroll--bounded': isMessagesTab }"
        >
          <div
            class="candidature-panel__layout"
            :class="{ 'candidature-panel__layout--full': !showAside }"
          >
            <CspTabsPanels
              :tabs="TABS"
              fill
              class="candidature-panel__main"
            >
              <template #candidature>
                <div class="candidature-panel__tab">
                  <CandidatureCv
                    v-if="candidature"
                    :candidature="candidatureParams"
                    :candidat-nom="title"
                  />
                </div>
              </template>
              <template #historique>
                <div class="candidature-panel__tab">
                  <CandidatureHistorique
                    v-if="candidature"
                    :candidature="candidatureParams"
                  />
                </div>
              </template>
              <template #documents>
                <div class="candidature-panel__tab">
                  <CandidatureDocuments
                    v-if="candidature"
                    :candidature="candidatureParams"
                  />
                </div>
              </template>

              <template #notes>
                <div class="candidature-panel__tab">
                  <CandidatureNotes
                    v-if="candidature"
                    :candidature="candidatureParams"
                  />
                </div>
              </template>

              <template #messages>
                <div class="candidature-panel__tab">
                  <MessagesSection
                    v-if="candidature"
                    :candidature="candidatureParams"
                    :candidat-nom="formatCandidatNom(candidature.candidat)"
                    :routes="panelRouteNames.conversations"
                  />
                </div>
              </template>
            </CspTabsPanels>
            <aside
              v-show="showAside"
              class="candidature-panel__aside"
              aria-label="Suivi de la candidature"
            >
              <template v-if="candidature">
                <CandidatureActivites
                  :candidature="candidatureParams"
                  :historique-route-name="panelRouteNames.tabs.historique"
                />
                <CspSeparator />
                <CandidatureNoteForm :candidature="candidatureParams" />
              </template>
            </aside>
          </div>
        </div>
      </CspTabs>
    </div>

    <template
      v-if="!loadFailed && !notFound"
      #footer
    >
      <CspSequenceNav
        :position="position ? position.index + 1 : null"
        :total="position?.total ?? 0"
        item-label="Candidature"
        :label="SEQUENCE_LABELS[view]"
        :previous-disabled="!position?.previousUuid"
        :next-disabled="!position?.nextUuid"
        @previous="goPrevious"
        @next="goNext"
      >
        <template v-if="etape">
          Étape : {{ etape.nom }}
        </template>
      </CspSequenceNav>
    </template>
  </CspDrawer>

  <RefusCandidatureDialog
    :open="etapeChange.refus.isOpen.value"
    :candidats="etapeChange.refus.candidats.value"
    :motifs="etapeChange.refus.motifs.value"
    :motifs-unavailable="etapeChange.refus.motifsUnavailable.value"
    @confirm="etapeChange.refus.confirm"
    @cancel="etapeChange.refus.cancel"
  />

  <CspUnsavedChangesDialog
    :open="unsavedChanges.isConfirming.value"
    @keep-editing="unsavedChanges.keepEditing"
    @leave="unsavedChanges.leave"
  />
</template>

<style lang="scss">
@use '@/styles/breakpoints' as bp;

/* unscoped: the drawer content is portaled */
.csp-drawer.candidature-panel {
  --base-drawer-width: 100vw;
  --csp-drawer-padding-inline: var(--csp-page-container-padding-inline);
  --csp-tabs-content-padding-inline: var(--csp-drawer-padding-inline);
  --candidature-panel-aside-padding-start: var(--csp-space-6);

  @include bp.from(bp.$lg) {
    --base-drawer-width: calc(100vw - 15rem);
  }

  @include bp.from(bp.$xl) {
    --base-drawer-width: clamp(42rem, 100vw - 36rem, 90rem);
  }

  .csp-drawer__body {
    display: flex;
    flex-direction: column;
    padding: 0;
    overflow: hidden;
  }

  .csp-drawer__footer {
    padding-block: var(--csp-space-3);
  }
}
</style>

<style scoped lang="scss">
.candidature-panel__exception {
  padding: var(--csp-page-content-padding-block) var(--csp-drawer-padding-inline);
}

.candidature-panel__body {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  container: panel / inline-size;
}

.candidature-panel__scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}

.candidature-panel__layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  min-height: 100%;
}

.candidature-panel__layout--full {
  grid-template-columns: minmax(0, 1fr);
}

.candidature-panel__scroll--bounded {
  overflow: hidden;
}

.candidature-panel__scroll--bounded .candidature-panel__layout {
  height: 100%;
  min-height: 0;
}

.candidature-panel__main {
  min-width: 0;
}

.candidature-panel__tab {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  padding: var(--csp-page-content-padding-block) var(--csp-drawer-padding-inline);
}

.candidature-panel__aside {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding-block: var(--csp-page-content-padding-block);
  padding-inline: var(--candidature-panel-aside-padding-start) var(--csp-drawer-padding-inline);
  border-left: 1px solid var(--border-default-grey);
}

@container panel (max-width: 64rem) {
  .candidature-panel__layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .candidature-panel__aside {
    padding-inline: var(--csp-drawer-padding-inline);
    border-top: 1px solid var(--border-default-grey);
    border-left: 0;
  }
}
</style>
