<script setup lang="ts">
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSidebar from '@/components/layout/CspSidebar/CspSidebar.vue'
import CspSidebarGroup from '@/components/layout/CspSidebar/CspSidebarGroup.vue'
import CspSidebarItem from '@/components/layout/CspSidebar/CspSidebarItem.vue'
import CspSidebarLogo from '@/components/layout/CspSidebar/CspSidebarLogo.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import CspSidebarUser from '@/components/layout/CspSidebar/CspSidebarUser.vue'
import { LIBELLES_STATUT, useOffre } from '../data/useOffre'
import ContextPanel from './ContextPanel.vue'
import StepNav from './StepNav.vue'

// Cadre de l'écran de création : navigation de l'ATS, barre de l'offre (statut, brouillon),
// étapes à gauche, contenu au centre, contexte du recrutement à droite.
const { state, step, dirty, saving, lastSaved, enregistrer, notifier, flash } = useOffre()

const statut = computed(() => LIBELLES_STATUT[state.statut])
const enDemarrage = computed(() => step.value === 'demarrer' && !state.startMode)

async function sauver() {
  await enregistrer()
  notifier('Brouillon enregistré. Vous pourrez le reprendre depuis « Mes offres ».')
}
</script>

<template>
  <CspSidebarProvider :default-expanded="false">
    <div class="co-app">
      <aside class="co-app__sidebar">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>
          <CspSidebarGroup>
            <CspSidebarItem
              icon="ri:dashboard-line"
              label="Tableau de bord"
              :to="{ path: '/tableau-de-bord' }"
            />
            <CspSidebarItem
              icon="ri:file-list-3-line"
              label="Besoins de recrutement"
              :to="{ path: '/besoins' }"
            />
            <CspSidebarItem
              icon="ri:briefcase-line"
              label="Offres"
              :to="{ path: '/offres' }"
              :is-active="true"
            />
            <CspSidebarItem
              icon="ri:team-line"
              label="Candidatures"
              :to="{ path: '/candidatures' }"
            />
          </CspSidebarGroup>
          <template #footer>
            <CspSidebarUser name="Camille Moreau" />
          </template>
        </CspSidebar>
      </aside>

      <div class="co-app__content">
        <header class="co-bar">
          <div class="co-bar__id">
            <p class="co-bar__crumb">
              Offres <span aria-hidden="true">›</span> {{ state.reference }}
            </p>
            <h1 class="co-bar__title">
              {{ state.besoin.intitule || 'Nouvelle offre' }}
            </h1>
          </div>
          <div class="co-bar__status">
            <CspBadge
              :label="statut.label"
              :type="statut.type"
              variant="soft"
              size="sm"
            />
            <span
              class="co-bar__save"
              aria-live="polite"
            >
              <template v-if="saving">
                <CspIcon
                  name="ri:loader-4-line"
                  class="co-spin"
                  :size="14"
                />
                Enregistrement…
              </template>
              <template v-else-if="dirty">
                <CspIcon
                  name="ri:edit-circle-line"
                  :size="14"
                />
                Modifications non enregistrées
              </template>
              <template v-else-if="lastSaved">
                <CspIcon
                  name="ri:check-line"
                  :size="14"
                />
                Enregistré {{ lastSaved }}
              </template>
            </span>
            <CspButton
              v-if="!enDemarrage && state.statut !== 'publiee'"
              label="Enregistrer le brouillon"
              variant="secondary"
              size="sm"
              icon="ri:save-3-line"
              is-icon-left
              :disabled="saving || !dirty"
              @click="sauver"
            />
          </div>
        </header>

        <div
          class="co-body"
          :class="{ 'co-body--start': enDemarrage }"
        >
          <div
            v-if="!enDemarrage"
            class="co-body__nav"
          >
            <StepNav />
          </div>
          <main class="co-main">
            <div class="co-main__inner">
              <slot />
            </div>
          </main>
          <div
            v-if="!enDemarrage"
            class="co-body__ctx"
          >
            <ContextPanel />
          </div>
        </div>
      </div>

      <div
        class="co-flash-region"
        aria-live="polite"
      >
        <div
          v-if="flash"
          class="co-flash"
          :class="`co-flash--${flash.variant}`"
        >
          <CspIcon
            :name="flash.variant === 'warning' ? 'ri:alert-line' : flash.variant === 'info' ? 'ri:information-line' : 'ri:checkbox-circle-line'"
            :size="16"
          />
          {{ flash.texte }}
        </div>
      </div>
    </div>
  </CspSidebarProvider>
</template>

<style scoped lang="scss">
.co-app {
  display: flex;
  height: 100vh;
  background: var(--background-default-grey);
  color: var(--text-default-grey);
}

.co-app__sidebar {
  flex-shrink: 0;
  height: 100vh;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);
}

.co-app__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.co-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-6);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.co-bar__id {
  min-width: 0;
}

.co-bar__crumb {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.co-bar__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  line-height: var(--csp-line-height-tight);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.co-bar__status {
  display: flex;
  align-items: center;
  gap: var(--csp-space-4);
  flex-shrink: 0;
}

.co-bar__save {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.co-body {
  display: grid;
  grid-template-columns: 15.5rem minmax(0, 1fr) 17rem;
  flex: 1;
  min-height: 0;

  &--start {
    grid-template-columns: minmax(0, 1fr);
  }
}

.co-body__nav {
  overflow-y: auto;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);
}

.co-body__ctx {
  overflow-y: auto;
  border-left: 1px solid var(--border-default-grey);
}

.co-main {
  overflow-y: auto;
  background: var(--background-alt-grey);
}

.co-main__inner {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 60rem;
  margin: 0 auto;
  padding: var(--csp-space-6) var(--csp-space-6) var(--csp-space-10);

  .co-body--start & {
    max-width: 68rem;
  }
}

.co-flash-region {
  position: fixed;
  bottom: var(--csp-space-6);
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--csp-z-toast, 50);
}

.co-flash {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-success);
  box-shadow: var(--csp-shadow-md);
  font-size: var(--csp-font-size-sm);

  &--info {
    border-left-color: var(--border-plain-info);
  }

  &--warning {
    border-left-color: var(--border-plain-warning);
  }
}

.co-spin {
  animation: co-spin 1s linear infinite;
}

@keyframes co-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
