<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import AtsSidebar from './AtsSidebar.vue'
import { useNav } from './nav'

// Cadre commun d'une page : navigation, fil d'Ariane, titre et actions, contenu, notification.
defineProps<{
  actif: 'accueil' | 'fiches' | 'offres' | 'parametres'
  titre: string
  sousTitre?: string
  fil?: { label: string, action?: () => void }[]
}>()
const { flash } = useNav()
</script>

<template>
  <CspSidebarProvider :default-expanded="true">
    <div class="ats">
      <AtsSidebar :actif="actif" />
      <main class="ats__main">
        <header class="ats__head">
          <div class="ats__id">
            <p
              v-if="fil?.length"
              class="ats__fil"
            >
              <template
                v-for="(f, i) in fil"
                :key="i"
              >
                <button
                  v-if="f.action"
                  type="button"
                  class="ats__lien"
                  @click="f.action"
                >
                  {{ f.label }}
                </button>
                <span v-else>{{ f.label }}</span>
                <span
                  v-if="i < fil.length - 1"
                  aria-hidden="true"
                > › </span>
              </template>
            </p>
            <div class="ats__titre-ligne">
              <h1 class="ats__titre">
                {{ titre }}
              </h1>
              <slot name="titre-fin" />
            </div>
            <p
              v-if="sousTitre"
              class="ats__sous"
            >
              {{ sousTitre }}
            </p>
          </div>
          <div class="ats__actions">
            <slot name="actions" />
          </div>
        </header>
        <slot name="sous-entete" />
        <div class="ats__contenu">
          <slot />
        </div>
      </main>
      <div
        class="ats__flash-zone"
        aria-live="polite"
      >
        <p
          v-if="flash"
          class="ats__flash"
        >
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="16"
          />
          {{ flash }}
        </p>
      </div>
    </div>
  </CspSidebarProvider>
</template>

<style scoped lang="scss">
.ats {
  display: flex;
  height: 100vh;
  background: var(--background-alt-grey);
  color: var(--text-default-grey);
}

.ats__main {
  flex: 1;
  min-width: 0;
  overflow-y: auto;
}

.ats__head {
  position: sticky;
  top: 0;
  z-index: 3;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-8);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.ats__id {
  min-width: 0;
}

.ats__fil {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.ats__lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.ats__titre-ligne {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  flex-wrap: wrap;
}

.ats__titre {
  margin: 0;
  font-size: var(--csp-font-size-xl);
  line-height: var(--csp-line-height-tight);
}

.ats__sous {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.ats__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}

.ats__contenu {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-6) var(--csp-space-8) var(--csp-space-12);
}

.ats__flash-zone {
  position: fixed;
  bottom: var(--csp-space-6);
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--csp-z-toast, 50);
}

.ats__flash {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-success);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
  font-size: var(--csp-font-size-sm);
}
</style>
