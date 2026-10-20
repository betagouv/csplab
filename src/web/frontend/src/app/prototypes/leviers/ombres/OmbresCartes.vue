<script setup lang="ts">
import type { LevierOption } from '../options'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import { valeursOf } from '../options'
import OmbresLoupe from './OmbresLoupe.vue'

defineProps<{
  options: LevierOption[]
}>()

const CANDIDATURES = demoKanban().etapes[0]!.candidatures.slice(0, 2)

// The story writes its color mode on the root element before it renders
const theme = document.documentElement.getAttribute('data-fr-theme') ?? 'light'
</script>

<template>
  <div
    class="ombres-cartes"
    :style="{ '--ombres-cartes-colonnes': options.length }"
  >
    <section
      v-for="option in options"
      :key="option.id"
      class="ombres-cartes__option"
      :style="valeursOf(option, theme)"
    >
      <h2 class="ombres-cartes__nom">
        {{ option.nom }}
      </h2>
      <div class="ombres-cartes__colonne">
        <CandidatureKanbanCard
          v-for="candidature in CANDIDATURES"
          :key="candidature.uuid"
          :candidature="candidature"
          :board-id="`ombres-${option.id}`"
          :column-id="`ombres-${option.id}`"
        />
      </div>
      <OmbresLoupe :candidature="CANDIDATURES[0]!" />
    </section>
  </div>
</template>

<style scoped lang="scss">
.ombres-cartes {
  display: grid;
  grid-template-columns: repeat(var(--ombres-cartes-colonnes), minmax(0, var(--csp-kanban-column-width)));
  place-content: center;
  gap: var(--csp-space-6);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-6);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.ombres-cartes__option {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  row-gap: var(--csp-space-3);
}

.ombres-cartes__nom {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-medium);
}

.ombres-cartes__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  padding: var(--csp-kanban-column-padding);
  background-color: var(--csp-region-background);
}
</style>
