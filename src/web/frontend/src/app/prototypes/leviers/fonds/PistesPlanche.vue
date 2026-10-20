<script setup lang="ts">
import type { FondSurfaceDessinee } from './planche'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { nomDeVariante, valeursDe } from './planche'

defineProps<{
  // The surface that the board compares
  surface: 'en-tete' | 'etat-vide'
  titre: string
  pistes: { nom: string, surface: FondSurfaceDessinee }[]
}>()

// The preview decorator writes the colour mode of the story on the root element before it renders
const sombre = document.documentElement.getAttribute('data-fr-theme') === 'dark'

const BREADCRUMB = [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements', to: '/' },
  { label: 'Gestionnaire des ressources humaines' },
]
</script>

<template>
  <div
    class="pistes-planche"
    :class="`pistes-planche--${surface}`"
  >
    <p class="pistes-planche__titre">
      {{ titre }}
    </p>
    <figure
      v-for="piste in pistes"
      :key="piste.nom"
      class="pistes-planche__piste"
    >
      <figcaption class="pistes-planche__legende">
        <span class="pistes-planche__nom">{{ piste.nom }}</span>
        <span
          v-if="piste.surface.variante"
          class="pistes-planche__variante"
        >{{ nomDeVariante(piste.surface.variante) }}</span>
      </figcaption>
      <div
        class="pistes-planche__surface"
        :style="valeursDe(piste.surface, sombre)"
      >
        <CspPageHeader
          v-if="surface === 'en-tete'"
          title="Gestionnaire des ressources humaines"
          subtitle="Créé le 26 septembre 2026, Lyon, catégorie B"
          :breadcrumb="BREADCRUMB"
          pictogram="document/document-search"
        />
        <CspEmptyState
          v-else
          icon="ri:file-list-line"
          pictogram="document/archive"
          title="La candidature ne contient aucun document"
        />
      </div>
    </figure>
  </div>
</template>

<style scoped lang="scss">
/* Page headers: one per row, close to their width on a screen of 1 280 px, so that a motif on the end edge keeps its
   distance from the title. Empty states: side by side. */
.pistes-planche {
  display: grid;
  align-content: center;
  gap: var(--csp-space-4);
  box-sizing: border-box;
  min-height: 100vh;
  padding: var(--csp-space-6);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.pistes-planche--etat-vide {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  column-gap: var(--csp-space-5);
}

.pistes-planche__titre {
  grid-column: 1 / -1;
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-mention-grey);
}

.pistes-planche__piste {
  display: grid;
  gap: var(--csp-space-2);
  min-width: 0;
  margin: 0;
}

.pistes-planche--en-tete .pistes-planche__piste {
  grid-template-columns: 12rem minmax(0, 1fr);
  align-items: center;
  gap: var(--csp-space-5);
}

.pistes-planche__legende {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.pistes-planche__nom {
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-medium);
}

.pistes-planche__variante {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

/* the values of a surface may change the text colours: its content reads them again */
.pistes-planche__surface {
  color: var(--text-default-grey);
}
</style>
