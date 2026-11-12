<script setup lang="ts" generic="T extends string = string">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import CspSidebarProvider from '@/components/layout/CspSidebar/CspSidebarProvider.vue'
import AtsSidebar from './AtsSidebar.vue'
import { useNav } from './nav'

// Cadre commun d'une page, calqué sur les pages de l'application : menu latéral, en-tête du design system
// (fil d'Ariane, retour, titre, sous-titre ou métadonnées, actions), onglets avec icônes, notification.
const props = withDefaults(defineProps<{
  actif: 'accueil' | 'fiches' | 'offres' | 'parametres'
  titre: string
  sousTitre?: string
  /** Fil d'Ariane après « Accueil » ; `to` est un chemin du menu (/fiches, /offres…). */
  fil?: { label: string, to?: string }[]
  /** Chemin du bouton retour, à gauche du titre. */
  retour?: { to: string, label: string }
  onglets?: CspTabItem<T>[]
  largeur?: 'wide' | 'full'
}>(), {
  sousTitre: undefined,
  fil: () => [],
  retour: undefined,
  onglets: undefined,
  largeur: 'wide',
})
const onglet = defineModel<T>('onglet')
const { flash } = useNav()

const ariane = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: props.actif === 'accueil' && !props.fil.length ? undefined : '/accueil' },
  ...props.fil,
])
</script>

<template>
  <CspSidebarProvider :default-expanded="true">
    <div
      class="ats"
      :class="{ 'ats--sans-onglets': !onglets }"
    >
      <AtsSidebar :actif="actif" />
      <div class="ats__main">
        <CspPageHeader
          :title="titre"
          :subtitle="sousTitre"
          :breadcrumb="ariane"
          :back-link="retour"
        >
          <template
            v-if="$slots.meta"
            #subtitle
          >
            <slot name="meta" />
          </template>
          <template
            v-if="$slots.actions"
            #actions
          >
            <div class="ats__actions">
              <slot name="actions" />
            </div>
          </template>
        </CspPageHeader>
        <CspPageContainer
          v-if="onglets"
          v-model:active-tab="onglet"
          :tabs="onglets"
          :width="largeur"
        >
          <template #tab>
            <div class="ats__contenu">
              <slot />
            </div>
          </template>
        </CspPageContainer>
        <CspPageContainer
          v-else
          :width="largeur"
        >
          <div class="ats__contenu">
            <slot />
          </div>
        </CspPageContainer>
      </div>
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
// Badges sans icône dans tout le prototype (demande d'Alice) : le libellé et la couleur suffisent.
.ats :deep(.badge > span:has(> .badge__icon)) {
  display: none;
}

// Sans onglets (page d'une offre, d'une fiche…), pas de filet sous l'en-tête.
.ats--sans-onglets :deep(.csp-page-header__main-row) {
  padding-bottom: 0;
  border-bottom: 0;
}

.ats {
  display: flex;
  height: 100vh;
  background: var(--background-default-grey);
  color: var(--text-default-grey);
}

.ats__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  overflow-y: auto;
}

.ats__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.ats__contenu {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding-bottom: var(--csp-space-12);
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
