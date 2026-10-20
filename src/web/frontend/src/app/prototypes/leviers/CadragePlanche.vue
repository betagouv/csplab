<script setup lang="ts">
import type { DeckInterfaceCadre } from '../DeckInterface.vue'
import DeckInterface from '../DeckInterface.vue'

export interface CadragePlancheEcran {
  // Id of the screen story
  story: string
  // Part of the screen, in its window of largeur x hauteur
  cadre: DeckInterfaceCadre
}

withDefaults(defineProps<{
  colonnes: string[]
  // Rows of parts of screens, one per column, with a caption when the rows differ
  rangees: { legende?: string, ecrans: CadragePlancheEcran[] }[]
  // Enlargement of each part
  echelle: number
  largeur?: number
  hauteur?: number
}>(), {
  largeur: 1440,
  hauteur: 900,
})
</script>

<template>
  <div
    class="cadrage-planche"
    :style="{ '--cadrage-planche-colonnes': colonnes.length }"
    :class="{ 'cadrage-planche--legendes': rangees.some(rangee => rangee.legende) }"
  >
    <span
      v-if="rangees.some(rangee => rangee.legende)"
      aria-hidden="true"
    />
    <span
      v-for="colonne in colonnes"
      :key="colonne"
      class="cadrage-planche__colonne"
    >{{ colonne }}</span>
    <template
      v-for="(rangee, index) in rangees"
      :key="index"
    >
      <span
        v-if="rangee.legende"
        class="cadrage-planche__rangee"
      >{{ rangee.legende }}</span>
      <DeckInterface
        v-for="(ecran, colonne) in rangee.ecrans"
        :key="colonne"
        class="cadrage-planche__ecran"
        planche="ecran"
        :ecran="ecran.story"
        :largeur="largeur"
        :hauteur="hauteur"
        :cadre="ecran.cadre"
        :style="{ width: `${Math.round(ecran.cadre.width * echelle)}px`, height: `${Math.round(ecran.cadre.height * echelle)}px` }"
      />
    </template>
  </div>
</template>

<style scoped lang="scss">
.cadrage-planche {
  display: grid;
  grid-template-columns: repeat(var(--cadrage-planche-colonnes), max-content);
  place-content: center;
  align-items: end;
  gap: var(--csp-space-4);
  box-sizing: border-box;
  min-height: 100vh;
  padding: var(--csp-space-5) var(--csp-space-6);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.cadrage-planche--legendes {
  grid-template-columns: max-content repeat(var(--cadrage-planche-colonnes), max-content);
}

.cadrage-planche__colonne,
.cadrage-planche__rangee {
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-medium);
}

/* a caption wraps within the width of the parts under it */
.cadrage-planche__colonne {
  width: 0;
  min-width: 100%;
}

.cadrage-planche__rangee {
  align-self: center;
  max-width: 7rem;
}

/* parts of different heights share the middle line of their row */
.cadrage-planche .cadrage-planche__ecran {
  align-self: center;
  box-shadow: 0 0 0 1px var(--border-default-grey);
}
</style>
