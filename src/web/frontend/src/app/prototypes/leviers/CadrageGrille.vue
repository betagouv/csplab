<script setup lang="ts">
import type { DeckInterfaceCadre } from '../DeckInterface.vue'
import DeckInterface from '../DeckInterface.vue'

withDefaults(defineProps<{
  // Screen stories, one per cell, which all show the same part of the screen
  ecrans: { story: string, legende: string }[]
  // Part of the screen, in its window of largeur x hauteur
  cadre: DeckInterfaceCadre
  // Enlargement of the part
  echelle: number
  colonnes: number
  largeur?: number
  hauteur?: number
}>(), {
  largeur: 1440,
  hauteur: 900,
})
</script>

<template>
  <div
    class="cadrage-grille"
    :style="{ '--cadrage-grille-colonnes': colonnes }"
  >
    <figure
      v-for="ecran in ecrans"
      :key="ecran.story"
      class="cadrage-grille__case"
    >
      <figcaption class="cadrage-grille__legende">
        {{ ecran.legende }}
      </figcaption>
      <DeckInterface
        class="cadrage-grille__ecran"
        planche="ecran"
        :ecran="ecran.story"
        :largeur="largeur"
        :hauteur="hauteur"
        :cadre="cadre"
        :style="{ width: `${Math.round(cadre.width * echelle)}px`, height: `${Math.round(cadre.height * echelle)}px` }"
      />
    </figure>
  </div>
</template>

<style scoped lang="scss">
.cadrage-grille {
  display: grid;
  grid-template-columns: repeat(var(--cadrage-grille-colonnes), max-content);
  place-content: center;
  gap: var(--csp-space-5) var(--csp-space-4);
  box-sizing: border-box;
  min-height: 100vh;
  padding: var(--csp-space-5) var(--csp-space-6);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

/* the captions of a row share their height, so that the parts under them line up */
.cadrage-grille__case {
  display: grid;
  grid-row: span 2;
  grid-template-rows: subgrid;
  row-gap: var(--csp-space-2);
  margin: 0;
}

/* a caption wraps within the width of the part under it */
.cadrage-grille__legende {
  width: 0;
  min-width: 100%;
  align-self: end;
  font-weight: var(--csp-font-weight-medium);
}

.cadrage-grille .cadrage-grille__ecran {
  box-shadow: 0 0 0 1px var(--border-default-grey);
}
</style>
