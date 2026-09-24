<script setup lang="ts">
import type { ScenarioKey } from '../data/scenario'
import type { SettingsArgs } from '../shared/settings'
import type { PersonId } from '../shared/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspSequenceNav from '@/components/base/CspSequenceNav/CspSequenceNav.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'
import { CANDIDATURE, PEOPLE, TABS } from '../data/scenario'
import { formatRelative, fullName } from '../shared/format'
import { resolveSettings } from '../shared/settings'
import { useMessagerie } from '../shared/useMessagerie'
import { useMessagesView } from '../shared/useMessagesView'
import ConversationList from '../thread/ConversationList.vue'
import ConversationThread from '../thread/ConversationThread.vue'

const props = defineProps<{
  settingsArgs: SettingsArgs
  pointDeVue: Extract<PersonId, 'jean-marc' | 'karim'>
  largeur: 'livree' | 'maquette'
  scenario: ScenarioKey
  conversationId?: string
  previousPeek?: number
}>()

const messagerie = useMessagerie(props.scenario)
if (props.conversationId)
  messagerie.selectedId.value = props.conversationId
const view = useMessagesView(messagerie, () => props.pointDeVue)
const settings = computed(() => resolveSettings(props.settingsArgs, 'recruteur'))
const tab = ref('messages')
const submitted = formatRelative(CANDIDATURE.soumiseLe, messagerie.clock.value)
</script>

<template>
  <CspDrawer
    :open="true"
    :modal="false"
    :show-close="false"
    aria-label="Candidature"
    class="recruiter-panel"
    :class="`recruiter-panel--${largeur}`"
    @interact-outside="(event: Event) => event.preventDefault()"
    @open-auto-focus="(event: Event) => event.preventDefault()"
  >
    <template #start>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:arrow-left-line"
        aria-label="Fermer la candidature et revenir au kanban"
      />
    </template>

    <template #end>
      <CspButton
        label="Changer d'étape"
        icon="ri:arrow-left-right-line"
        is-icon-left
        size="sm"
      />
    </template>

    <template #title>
      {{ fullName(PEOPLE.camille) }}
    </template>

    <template #description>
      Candidature {{ submitted }}
    </template>

    <div class="recruiter-panel__body">
      <CspTabs
        v-model="tab"
        fill
        class="recruiter-panel__tabs"
      >
        <CspTabsList :tabs="TABS" />
        <CspTabsPanels
          :tabs="TABS"
          fill
        >
          <template #messages>
            <div class="recruiter-panel__messages">
              <div class="recruiter-panel__frame">
                <ConversationList
                  :summaries="messagerie.summaries.value"
                  :viewer-id="pointDeVue"
                  :selected-id="messagerie.selectedId.value"
                  :unread-ids="view.unreadIds.value"
                  :dates="settings.dates"
                  :now="messagerie.clock.value"
                  can-create
                  class="recruiter-panel__list"
                  @select="view.select"
                />
                <ConversationThread
                  v-if="view.current.value"
                  :key="view.current.value.id"
                  :conversation="view.current.value"
                  :messages="view.currentMessages.value"
                  :viewer-id="pointDeVue"
                  viewer="recruteur"
                  :settings="settings"
                  :now="messagerie.clock.value"
                  :waiting="view.currentWaiting.value"
                  :previous-peek="previousPeek"
                  @send="view.send"
                  @choose="view.choose"
                  @mark-unread="view.markUnread"
                />
              </div>
            </div>
          </template>
        </CspTabsPanels>
      </CspTabs>
    </div>

    <template #footer>
      <CspSequenceNav
        :position="CANDIDATURE.position"
        :total="CANDIDATURE.total"
        item-label="Candidature"
        label="Navigation entre les candidatures de l’étape"
      >
        Étape : {{ CANDIDATURE.etape }}
      </CspSequenceNav>
    </template>
  </CspDrawer>
</template>

<style lang="scss">
@use '@/styles/breakpoints' as bp;

/* unscoped: the drawer content is portaled */
.csp-drawer.recruiter-panel {
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

  .recruiter-panel__tabs .csp-tabs__list {
    padding-inline: calc(var(--csp-page-container-padding-inline) - 1rem);
    border-bottom: 1px solid var(--border-default-grey);
  }

  .recruiter-panel__tabs .csp-tabs__trigger {
    white-space: nowrap;
  }

  .csp-drawer__footer {
    padding: var(--csp-space-3) var(--csp-page-container-padding-inline);
  }
}

.csp-drawer.recruiter-panel--maquette {
  --base-drawer-width: 69.375rem;

  @include bp.from(bp.$lg) {
    --base-drawer-width: 69.375rem;
  }

  @include bp.from(bp.$xl) {
    --base-drawer-width: 69.375rem;
  }
}
</style>

<style scoped>
.recruiter-panel__body {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  container: panel / inline-size;
}

.recruiter-panel__messages {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  padding: var(--csp-page-content-padding-block) var(--csp-page-container-padding-inline);
}

.recruiter-panel__frame {
  display: grid;
  flex: 1;
  grid-template-columns: 17.5rem minmax(0, 1fr);
  min-height: 0;
  border: 1px solid var(--border-default-grey);
}

.recruiter-panel__list {
  border-right: 1px solid var(--border-default-grey);
}
</style>
