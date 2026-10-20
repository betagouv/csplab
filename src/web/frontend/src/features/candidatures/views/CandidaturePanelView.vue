<script setup lang="ts">
import type { CandidaturePanelTabKey } from '../constants/candidature'
import type { CandidaturesViewName } from '@/router/names'
import { useQueryCache } from '@pinia/colada'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
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
import CandidatureActivites from '../components/CandidatureActivites.vue'
import CandidatureCv from '../components/CandidatureCv.vue'
import CandidatureDocuments from '../components/CandidatureDocuments.vue'
import CandidatureEtiquettes from '../components/CandidatureEtiquettes.vue'
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
import { etiquettesOf } from '../etiquettes'
import { formatCandidatName, formatCandidatureMeta } from '../format'
import { candidatureDetailQuery } from '../queries'

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

const title = computed(() => candidature.value ? formatCandidatName(candidature.value.candidat) : 'Candidature')
const description = computed(() => candidature.value?.recrutement_intitule || null)
const metaItems = computed(() => candidature.value ? formatCandidatureMeta(candidature.value) : [])
const etiquettes = computed(() => candidature.value ? etiquettesOf(candidature.value) : [])

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
  () => candidature.value && formatCandidatName(candidature.value.candidat),
)
const TABS_WITHOUT_ASIDE: CandidaturePanelTabKey[] = ['historique', 'messages']
const isMessagesTab = computed(() => activeTab.value === 'messages')
const isNotesTab = computed(() => activeTab.value === 'notes')
const showAside = computed(() => !TABS_WITHOUT_ASIDE.includes(activeTab.value))

const unsavedChanges = useUnsavedChangesGuard({
  ignore: to => to.params.candidatureUuid === props.candidatureUuid,
})

// The drawer plays its exit animation, then reka-ui unmounts its content and emits close-auto-focus
const isOpen = ref(true)
watch(() => props.candidatureUuid, () => {
  isOpen.value = true
})

async function close(): Promise<void> {
  if (await unsavedChanges.confirmLeave()) {
    isOpen.value = false
  }
}

function leaveAfterExit(): void {
  if (!isOpen.value) {
    void router.push({ name: parentName.value })
  }
}

function leaveMovedCandidature(): void {
  if (position.value?.nextUuid) {
    navigation.navigateTo(position.value.nextUuid)
  }
  else {
    void close()
  }
}

const etapeChange = useEtapeChange(
  () => ({ organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid }),
  candidature,
  leaveMovedCandidature,
)

async function requestEtapeChange(targetEtapeUuid: string): Promise<void> {
  if (await unsavedChanges.confirmLeave()) {
    etapeChange.request(targetEtapeUuid)
  }
}

function handleUpdateOpen(open: boolean): void {
  if (!open) {
    void close()
  }
}
</script>

<template>
  <CspDrawer
    :open="isOpen"
    :overlay="false"
    aria-label="Candidature"
    close-label="Fermer la candidature"
    class="candidature-panel"
    @update:open="handleUpdateOpen"
    @close-auto-focus="leaveAfterExit"
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
      v-if="!showSkeleton && etape"
      #title-end
    >
      <CspBadge
        class="candidature-panel__etape"
        :label="etape.nom"
      />
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

    <template
      v-if="!showSkeleton && metaItems.length"
      #meta
    >
      <CspMetaList :items="metaItems" />
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
        pictogram="system/padlock"
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
                    :routes="panelRouteNames.notes"
                  />
                </div>
              </template>

              <template #messages>
                <div class="candidature-panel__tab">
                  <MessagesSection
                    v-if="candidature"
                    :candidature="candidatureParams"
                    :candidat-nom="formatCandidatName(candidature.candidat)"
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
                <CandidatureEtiquettes :etiquettes="etiquettes" />
                <CspSeparator v-show="!isNotesTab" />
                <CandidatureNoteForm
                  v-show="!isNotesTab"
                  :candidature="candidatureParams"
                />
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

/* On a wide screen, --csp-panel-page-offset keeps the width of the open panel free beside the page: the panel becomes
   a surface next to the board, and --csp-panel-shadow-docked replaces its shadow */
@media (min-width: 105rem) {
  body:has(.csp-drawer.candidature-panel) .csp-app-shell__content {
    padding-right: var(--csp-panel-page-offset);
  }

  .csp-drawer.candidature-panel {
    box-shadow: var(--csp-panel-shadow-docked);
  }

  .csp-drawer.candidature-panel.csp-drawer--right {
    --base-drawer-width: var(--csp-panel-width-docked);

    background-color: var(--csp-panel-background-docked);
    top: var(--csp-panel-inset-docked);
    right: var(--csp-panel-inset-docked);
    bottom: var(--csp-panel-inset-docked);
    border-style: solid;
    border-width: var(--csp-panel-border-width-docked);
  }
}

/* above tabs the line under the header takes its own width, and framed tabs draw it themselves */
.csp-drawer.candidature-panel:has(.candidature-panel__tabs) {
  --csp-drawer-header-border-width: calc((1 - var(--csp-tabs-framed)) * var(--csp-panel-header-border-width-tabs));
}

/* unscoped: the drawer content is portaled */
.csp-drawer.candidature-panel {
  --base-drawer-width: 100vw;
  --csp-drawer-padding-inline: var(--csp-page-container-padding-inline);
  --csp-tabs-content-padding-inline: var(--csp-drawer-padding-inline);
  --candidature-panel-aside-padding-start: var(--csp-space-6);
  --csp-drawer-background: var(--csp-panel-chrome-background);
  --csp-drawer-header-backdrop: var(--csp-panel-header-backdrop);

  @include bp.from(bp.$md) {
    --csp-tabs-list-divider-box: var(--csp-page-tabs-divider-box);
  }

  @include bp.from(bp.$lg) {
    --base-drawer-width: calc(100vw - 15rem);
  }

  @include bp.from(bp.$xl) {
    --base-drawer-width: var(--csp-panel-width-wide);
  }

  @include bp.from(bp.$md) {
    --csp-tabs-content-padding-inline: calc(var(--csp-drawer-padding-inline) - var(--csp-panel-tabs-inset));
  }

  .candidature-panel__tabs > .csp-tabs__list {
    @include bp.from(bp.$md) {
      margin-inline: var(--csp-panel-tabs-inset);
    }
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
@use '@/styles/breakpoints' as bp;
@use '@/styles/scroll-edges.scss' as edges;

.candidature-panel__etape {
  align-self: center;
  margin: 0;
}

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
  overscroll-behavior: contain;
  background-color: var(--csp-panel-background);

  @include edges.scroll-edges($rule: false);
}

.candidature-panel__layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 20rem;
  min-height: 100%;
}

.candidature-panel__layout--full {
  grid-template-columns: minmax(0, 1fr);
}

/* forced colours remove the gradient line under framed tabs */
@media (forced-colors: active) {
  .candidature-panel__scroll {
    border-top: calc(var(--csp-tabs-framed) * 1px) solid;
  }
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
  background-color: var(--csp-aside-background);
  border-left: 1px solid var(--csp-aside-border-color);
}

@container panel (max-width: 64rem) {
  .candidature-panel__layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .candidature-panel__aside {
    padding-inline: var(--csp-drawer-padding-inline);
    border-top: 1px solid var(--csp-aside-border-color);
    border-left: 0;

    @include bp.from(bp.$md) {
      margin-inline: var(--csp-panel-aside-inset);
      padding-inline: calc(var(--csp-drawer-padding-inline) - var(--csp-panel-aside-inset));
    }
  }
}
</style>
