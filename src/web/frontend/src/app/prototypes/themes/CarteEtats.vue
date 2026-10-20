<script setup lang="ts">
import type { OmbresEtat } from '../leviers/ombres/OmbresCarte.vue'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import OmbresCarte from '../leviers/ombres/OmbresCarte.vue'

// A card of the kanban in each of its states, in a column of the interface theme applied to the page
const CANDIDATURE = demoKanban().etapes[0]!.candidatures[0]!

const ETATS: { etat: OmbresEtat, legende: string }[] = [
  { etat: 'repos', legende: 'Au repos' },
  { etat: 'survol', legende: 'Au survol' },
  { etat: 'focus', legende: 'Focus clavier' },
  { etat: 'glisser', legende: 'Pendant le glisser' },
  { etat: 'depose', legende: 'Déposée dans une autre colonne' },
]
</script>

<template>
  <div class="carte-etats">
    <div
      v-for="({ etat, legende }, index) in ETATS"
      :key="etat"
      class="carte-etats__etat"
    >
      <span class="carte-etats__legende">{{ legende }}</span>
      <OmbresCarte
        :etat="etat"
        :candidature="CANDIDATURE"
        :card-index="index"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.carte-etats {
  display: grid;
  grid-template-columns: repeat(3, var(--csp-kanban-column-width));
  place-content: center;
  gap: var(--csp-space-8) var(--csp-space-6);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--csp-region-background);
  color: var(--text-default-grey);
}

.carte-etats__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.carte-etats__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
