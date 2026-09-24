<script setup lang="ts">
import type { ScenarioKey } from '../data/scenario'
import type { SettingsArgs } from '../shared/settings'
import { computed, onMounted, ref, useId } from 'vue'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { CANDIDATURE, PEOPLE } from '../data/scenario'
import { formatDayWithYear, fullName } from '../shared/format'
import { resolveSettings } from '../shared/settings'
import { useMessagerie } from '../shared/useMessagerie'
import { useMessagesView } from '../shared/useMessagesView'
import ConversationList from '../thread/ConversationList.vue'
import ConversationThread from '../thread/ConversationThread.vue'
import ProgressSteps from './ProgressSteps.vue'

const props = withDefaults(defineProps<{
  settingsArgs: SettingsArgs
  scenario: ScenarioKey
  ouverture?: 'haut' | 'dernier-message' | 'demande'
}>(), {
  ouverture: 'haut',
})

const OPENING_TARGETS = {
  'dernier-message': '.conversation-thread__scroll ol > li:last-child',
  'demande': '.slot-request',
}

onMounted(() => {
  if (props.ouverture === 'haut')
    return
  const selector = OPENING_TARGETS[props.ouverture]
  setTimeout(() => {
    const target = document.querySelector(selector)
    if (target)
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 16 })
  }, 100)
})

const messagerie = useMessagerie(props.scenario)
const view = useMessagesView(messagerie, () => 'camille')
const settings = computed(() => resolveSettings(props.settingsArgs, 'candidat'))
const messagesTitleId = useId()
const pane = ref<'liste' | 'fil'>('fil')

const breadcrumb = [
  { label: 'Accueil', to: '/' },
  { label: 'Mes candidatures', to: '/' },
  { label: CANDIDATURE.offre },
]

function open(id: string): void {
  view.select(id)
  pane.value = 'fil'
}
</script>

<template>
  <div class="candidate-space">
    <header class="candidate-space__header">
      <div class="candidate-space__header-inner">
        <p class="candidate-space__logo">
          République<br>française
        </p>
        <p class="candidate-space__service">
          Choisir le service public
        </p>
        <p class="candidate-space__account">
          {{ fullName(PEOPLE.camille) }}
        </p>
      </div>
    </header>

    <main class="candidate-space__main">
      <CspBreadcrumb :items="breadcrumb" />

      <div class="candidate-space__intro">
        <h1 class="candidate-space__title">
          {{ CANDIDATURE.offre }}
        </h1>
        <p class="candidate-space__meta">
          {{ CANDIDATURE.service }} · Candidature envoyée le {{ formatDayWithYear(CANDIDATURE.soumiseLe) }}
        </p>
      </div>

      <ProgressSteps
        v-if="settings.progress"
        :steps="CANDIDATURE.etapes"
        :current-index="CANDIDATURE.etapeIndex"
        class="candidate-space__progress"
      />

      <section
        class="candidate-space__messages"
        :aria-labelledby="messagesTitleId"
      >
        <h2
          :id="messagesTitleId"
          class="candidate-space__section-title"
        >
          Messages de l’équipe de recrutement
        </h2>
        <div
          class="candidate-space__frame"
          :class="`candidate-space__frame--${pane}`"
        >
          <ConversationList
            :summaries="messagerie.summaries.value"
            viewer-id="camille"
            :selected-id="messagerie.selectedId.value"
            :unread-ids="view.unreadIds.value"
            :dates="settings.dates"
            :now="messagerie.clock.value"
            :can-create="false"
            class="candidate-space__list"
            @select="open"
          />
          <div class="candidate-space__thread">
            <div class="candidate-space__back">
              <CspButton
                variant="tertiary-no-outline"
                size="sm"
                label="Toutes les conversations"
                icon="ri:arrow-left-line"
                is-icon-left
                @click="pane = 'liste'"
              />
            </div>
            <ConversationThread
              v-if="view.current.value"
              :key="view.current.value.id"
              :conversation="view.current.value"
              :messages="view.currentMessages.value"
              viewer-id="camille"
              viewer="candidat"
              :settings="settings"
              :now="messagerie.clock.value"
              :waiting="view.currentWaiting.value"
              @send="view.send"
              @choose="view.choose"
            />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.candidate-space {
  min-height: 100vh;
  background: var(--background-default-grey);
  container: space / inline-size;
}

.candidate-space__header {
  border-bottom: 1px solid var(--border-default-grey);
  box-shadow: var(--csp-shadow-sm);
}

.candidate-space__header-inner {
  display: flex;
  gap: var(--csp-space-6);
  align-items: center;
  max-width: var(--csp-page-container-reading-width);
  margin: 0 auto;
  padding: var(--csp-space-4) var(--csp-page-container-padding-inline);
}

.candidate-space__logo {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.1;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.candidate-space__service {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
}

.candidate-space__account {
  margin: 0 0 0 auto;
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
}

.candidate-space__main {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  max-width: var(--csp-page-container-reading-width);
  margin: 0 auto;
  padding: var(--csp-space-6) var(--csp-page-container-padding-inline) var(--csp-space-12);
}

.candidate-space__intro {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.candidate-space__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
  font-weight: var(--csp-font-weight-bold);
  line-height: var(--csp-line-height-tight);
  color: var(--text-title-grey);
}

.candidate-space__meta {
  margin: 0;
  color: var(--text-mention-grey);
}

.candidate-space__progress {
  max-width: 34rem;
}

.candidate-space__messages {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.candidate-space__section-title {
  margin: 0;
  font-size: var(--csp-font-size-xl);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidate-space__frame {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  height: 44rem;
  border: 1px solid var(--border-default-grey);
}

.candidate-space__list {
  border-right: 1px solid var(--border-default-grey);
}

.candidate-space__thread {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.candidate-space__back {
  display: none;
}

@container space (max-width: 48rem) {
  .candidate-space__header-inner {
    flex-wrap: wrap;
    gap: var(--csp-space-2) var(--csp-space-4);
  }

  .candidate-space__service {
    font-size: var(--csp-font-size-md);
  }

  .candidate-space__account {
    display: none;
  }

  .candidate-space__frame {
    display: block;
    height: auto;
    border: 0;
  }

  .candidate-space__frame--fil .candidate-space__list,
  .candidate-space__frame--liste .candidate-space__thread {
    display: none;
  }

  .candidate-space__list {
    border: 1px solid var(--border-default-grey);
  }

  .candidate-space__back {
    display: block;
    margin-bottom: var(--csp-space-2);
  }

  .candidate-space__thread :deep(.conversation-thread) {
    height: auto;
    border: 1px solid var(--border-default-grey);
  }

  .candidate-space__thread :deep(.conversation-thread__scroll) {
    overflow: visible;
  }

  .candidate-space__thread :deep(.reply-zone) {
    position: sticky;
    bottom: 0;
    border-top: 1px solid var(--border-default-grey);
  }
}
</style>
