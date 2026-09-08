<script setup lang="ts">
import type { PanelTab } from '../shared/useCandidaturePrototype'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed } from 'vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import { useCandidaturePrototypeContext } from '../shared/context'
import ColonneDroite from './ColonneDroite.vue'
import OngletCandidature from './OngletCandidature.vue'
import OngletDocuments from './OngletDocuments.vue'
import OngletHistorique from './OngletHistorique.vue'
import OngletMessages from './OngletMessages.vue'
import OngletNotes from './OngletNotes.vue'
import PanelFooter from './PanelFooter.vue'
import PanelHeader from './PanelHeader.vue'

const proto = useCandidaturePrototypeContext()

const TABS: CspTabItem<PanelTab>[] = [
  { value: 'candidature', label: 'Candidature', icon: 'ri:user-line' },
  { value: 'historique', label: 'Historique d\'activité', icon: 'ri:history-line' },
  { value: 'documents', label: 'Documents', icon: 'ri:file-list-line' },
  { value: 'notes', label: 'Notes', icon: 'ri:sticky-note-line' },
  { value: 'messages', label: 'Messages', icon: 'ri:chat-3-line' },
]

const isOpen = computed(() => proto.candidature.value !== null)

function handleUpdateOpen(open: boolean): void {
  if (!open)
    proto.close()
}

function isEditing(target: EventTarget | null): boolean {
  return target instanceof HTMLElement
    && (target.matches('input, textarea, select, [contenteditable="true"]'))
}

function handleKeydown(event: KeyboardEvent): void {
  if (isEditing(event.target) || event.metaKey || event.ctrlKey || event.altKey)
    return
  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    proto.goPrevious()
  }
  if (event.key === 'ArrowRight') {
    event.preventDefault()
    proto.goNext()
  }
}
</script>

<template>
  <CspDrawer
    :open="isOpen"
    :modal="false"
    :show-close="false"
    :style="{ '--base-drawer-width': 'calc(100vw - 21rem)' }"
    class="candidature-panel"
    aria-label="Candidature"
    @update:open="handleUpdateOpen"
    @interact-outside="(event: Event) => event.preventDefault()"
    @keydown="handleKeydown"
  >
    <template
      v-if="proto.candidature.value"
      #title
    >
      <PanelHeader
        :candidature="proto.candidature.value"
        :etape-courante="proto.etapeCourante.value"
        :etapes="proto.scenario.etapes"
        @close="proto.close()"
        @changer-etape="proto.changerEtape($event)"
        @copier-lien="proto.copierLien()"
      />
    </template>

    <div
      v-if="proto.candidature.value"
      class="candidature-panel__layout"
    >
      <div class="candidature-panel__main">
        <CspTabs
          v-model="proto.tab.value"
          :tabs="TABS"
          class="candidature-panel__tabs"
        >
          <template #candidature>
            <div class="candidature-panel__tab">
              <OngletCandidature :candidature="proto.candidature.value" />
            </div>
          </template>
          <template #historique>
            <div class="candidature-panel__tab">
              <OngletHistorique :candidature="proto.candidature.value" />
            </div>
          </template>
          <template #documents>
            <div class="candidature-panel__tab">
              <OngletDocuments :candidature="proto.candidature.value" />
            </div>
          </template>
          <template #notes>
            <div class="candidature-panel__tab">
              <OngletNotes
                v-model:note-draft="proto.noteDraft.value"
                v-model:note-privee="proto.notePrivee.value"
                :candidature="proto.candidature.value"
                @submit-draft="proto.saveNote()"
                @update="(uuid, patch) => proto.updateNote(uuid, patch)"
                @delete="proto.deleteNote($event)"
              />
            </div>
          </template>
          <template #messages>
            <div class="candidature-panel__tab">
              <OngletMessages />
            </div>
          </template>
        </CspTabs>
      </div>
      <ColonneDroite
        v-model:note-draft="proto.noteDraft.value"
        v-model:note-privee="proto.notePrivee.value"
        v-model:tag-picker-open="proto.tagPickerOpen.value"
        class="candidature-panel__aside"
        :candidature="proto.candidature.value"
        @voir-tout="proto.tab.value = 'historique'"
        @add-tag="proto.addTag($event)"
        @remove-tag="proto.removeTag($event)"
        @save-note="proto.saveNote()"
      />
    </div>

    <template #footer>
      <PanelFooter
        :etape-nom="proto.etapeCourante.value?.nom ?? null"
        :position="proto.position.value"
        @previous="proto.goPrevious()"
        @next="proto.goNext()"
      />
    </template>
  </CspDrawer>
</template>

<style lang="scss">
.candidature-panel .csp-drawer__header {
  padding: var(--csp-space-5) var(--csp-space-6) var(--csp-space-3);
  border-bottom: 0;
}

.candidature-panel .csp-drawer__heading {
  flex: 1;
}

.candidature-panel .csp-drawer__title {
  width: 100%;
}

.candidature-panel .csp-drawer__body {
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.candidature-panel .csp-drawer__footer {
  padding: var(--csp-space-3) var(--csp-space-6);
}
</style>

<style scoped lang="scss">
.candidature-panel__layout {
  --panel-gutter: var(--csp-space-6);
  --panel-aside-width: 20rem;

  display: grid;
  flex: 1;
  grid-template-columns: minmax(0, 1fr) var(--panel-aside-width);
  min-height: 0;
}

.candidature-panel__main {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
}

.candidature-panel__tabs :deep(.csp-tabs__list) {
  position: sticky;
  top: 0;
  z-index: 1;
  padding-inline: calc(var(--panel-gutter) - 1rem);
  background: var(--background-overlap-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.candidature-panel__tabs :deep(.csp-tabs__trigger) {
  white-space: nowrap;
}

.candidature-panel__tab {
  padding: var(--csp-space-5) var(--panel-gutter) var(--csp-space-6);
}

.candidature-panel__aside {
  min-height: 0;
  overflow-y: auto;
  padding: var(--csp-space-5) var(--panel-gutter) var(--csp-space-6);
  border-left: 1px solid var(--border-default-grey);
}

@media (width <= 85em) {
  .candidature-panel__layout {
    grid-template-columns: minmax(0, 1fr);
    overflow-y: auto;
  }

  .candidature-panel__main {
    overflow: visible;
  }

  .candidature-panel__aside {
    overflow: visible;
    border-top: 1px solid var(--border-default-grey);
    border-left: 0;
  }
}
</style>
