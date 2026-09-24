<script setup lang="ts">
import type { Candidature } from '../types'
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspSequenceNav from '@/components/base/CspSequenceNav/CspSequenceNav.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { tabItems } from '@/composables/navigation/tabs'
import { useReturnTo } from '@/composables/navigation/useReturnTo'
import { useRouteTab } from '@/composables/navigation/useRouteTab'
import { formatDateLong, formatElapsedDays } from '@/utils/date'
import ChangerEtapePopover from '../components/ChangerEtapePopover.vue'
import RefusCandidatureDialog from '../components/RefusCandidatureDialog.vue'
import { useCandidatureNavigation } from '../composables/useCandidatureNavigation'
import { useCandidatures } from '../composables/useCandidatures'
import { useEtapeChange } from '../composables/useEtapeChange'
import { CANDIDATURE_PANEL_TAB_ICONS, CANDIDATURE_PANEL_TAB_LABELS } from '../constants/candidature'
import { CANDIDATURE_PANEL_TAB_ROUTE_NAMES } from '../routes'
import { formatCandidatNom } from '../utils/candidat'

const route = useRoute()

const { findCandidature, pendingKanban, error } = useCandidatures()

const candidatureUuid = computed(() => route.params.candidatureUuid as string)
const candidature = computed<Candidature | null>(() => findCandidature(candidatureUuid.value))

const showSkeleton = useMinimumPending(computed(() => pendingKanban.value && !candidature.value))
const loadFailed = computed(() => !pendingKanban.value && Boolean(error.value))
const isNotFound = computed(() => !pendingKanban.value && !error.value && !candidature.value)

const title = computed(() => candidature.value ? formatCandidatNom(candidature.value.candidat) : 'Candidature')
const description = computed(() =>
  candidature.value ? `Candidature ${formatElapsedDays(candidature.value.date_soumission)}` : null,
)

const { position, etape, goPrevious, goNext } = useCandidatureNavigation(candidatureUuid)

const scrollArea = ref<HTMLElement | null>(null)
watch(candidatureUuid, () => {
  if (scrollArea.value)
    scrollArea.value.scrollTop = 0
})

const TABS = tabItems(CANDIDATURE_PANEL_TAB_LABELS, CANDIDATURE_PANEL_TAB_ICONS)
const activeTab = useRouteTab(CANDIDATURE_PANEL_TAB_ROUTE_NAMES, 'candidature')

const close = useReturnTo(() => ({
  name: 'recrutement-candidatures-kanban',
  params: { organismeUuid: route.params.organismeUuid, recrutementUuid: route.params.recrutementUuid },
}))

const etapeChange = useEtapeChange(candidatureUuid, close)

function handleUpdateOpen(open: boolean): void {
  if (!open)
    close()
}
</script>

<template>
  <CspDrawer
    :open="true"
    :modal="false"
    :show-close="false"
    aria-label="Candidature"
    class="candidature-panel"
    @update:open="handleUpdateOpen"
    @interact-outside="(event: Event) => event.preventDefault()"
  >
    <template #start>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:arrow-left-line"
        aria-label="Fermer la candidature et revenir au kanban"
        @click="close"
      />
    </template>

    <template
      v-if="candidature && etape"
      #end
    >
      <ChangerEtapePopover
        :etapes="etapeChange.etapes.value"
        :current-etape-uuid="etape.etape_uuid"
        @confirm="etapeChange.request"
      />
    </template>

    <template #title>
      <CspSkeleton
        v-if="showSkeleton"
        width="12rem"
        height="1.375rem"
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
        height="1.25rem"
      />
      <template v-else>
        {{ description }}
      </template>
    </template>

    <div
      v-if="loadFailed || isNotFound"
      class="candidature-panel__exception"
    >
      <CspErrorState
        v-if="loadFailed"
        title="Une erreur est survenue lors du chargement de la candidature."
      />
      <CspEmptyState
        v-else
        icon="ri:search-line"
        title="Candidature introuvable"
        description="Cette candidature n'existe pas ou n'est plus accessible."
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
        >
          <div class="candidature-panel__layout">
            <CspTabsPanels
              :tabs="TABS"
              fill
              class="candidature-panel__main"
            >
              <template #candidature>
                <div class="candidature-panel__tab">
                  <dl
                    v-if="candidature"
                    class="candidature-panel__summary"
                  >
                    <dt>Candidat</dt>
                    <dd>{{ title }}</dd>
                    <dt>Candidature déposée le</dt>
                    <dd>{{ formatDateLong(candidature.date_soumission) }}</dd>
                  </dl>
                </div>
              </template>
            </CspTabsPanels>
            <aside
              class="candidature-panel__aside"
              aria-label="Suivi de la candidature"
            >
              <p class="candidature-panel__placeholder">
                Activités, tags et note (à venir)
              </p>
            </aside>
          </div>
        </div>
      </CspTabs>
    </div>

    <template
      v-if="!loadFailed && !isNotFound"
      #footer
    >
      <CspSequenceNav
        :position="position ? position.index + 1 : null"
        :total="position?.total ?? 0"
        item-label="Candidature"
        label="Navigation entre les candidatures de l'étape"
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
</template>

<style lang="scss">
@use '@/styles/breakpoints' as bp;

/* unscoped: the drawer content is portaled */
.csp-drawer.candidature-panel {
  --base-drawer-width: 100vw;

  @include bp.from(bp.$lg) {
    --base-drawer-width: calc(100vw - 15rem);
  }

  @include bp.from(bp.$xl) {
    --base-drawer-width: clamp(42rem, 100vw - 36rem, 90rem);
  }

  .csp-drawer__header {
    border-bottom: 0;
  }

  .csp-drawer__body {
    display: flex;
    flex-direction: column;
    padding: 0;
    overflow: hidden;
  }

  .candidature-panel__tabs .csp-tabs__list {
    padding-inline: calc(var(--csp-page-container-padding-inline) - 1rem);
    border-bottom: 1px solid var(--border-default-grey);
  }

  .csp-drawer__footer {
    padding: var(--csp-space-3) var(--csp-page-container-padding-inline);
  }

  .candidature-panel__tabs .csp-tabs__trigger {
    white-space: nowrap;
  }
}
</style>

<style scoped lang="scss">
.candidature-panel__exception {
  padding: var(--csp-page-content-padding-block) var(--csp-page-container-padding-inline);
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

.candidature-panel__main {
  min-width: 0;
}

.candidature-panel__tab {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: var(--csp-page-content-padding-block) var(--csp-page-container-padding-inline);
}

.candidature-panel__summary {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: var(--csp-space-2) var(--csp-space-4);
  margin: 0;

  dt {
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
  }
}

.candidature-panel__aside {
  padding: var(--csp-page-content-padding-block) var(--csp-page-container-padding-inline);
  border-left: 1px solid var(--border-default-grey);
}

.candidature-panel__placeholder {
  margin: 0;
  color: var(--text-mention-grey);
}

@container panel (max-width: 64rem) {
  .candidature-panel__layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .candidature-panel__aside {
    border-top: 1px solid var(--border-default-grey);
    border-left: 0;
  }
}
</style>
