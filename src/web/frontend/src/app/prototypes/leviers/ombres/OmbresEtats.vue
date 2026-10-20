<script setup lang="ts">
import type { OmbresEtat } from './OmbresCarte.vue'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import OmbresCarte from './OmbresCarte.vue'

const CANDIDATURE = demoKanban().etapes[0]!.candidatures[0]!

const ETATS: { etat: OmbresEtat, legende: string }[] = [
  { etat: 'repos', legende: 'Au repos' },
  { etat: 'survol', legende: 'Au survol' },
  { etat: 'focus', legende: 'Focus clavier' },
  { etat: 'glisser', legende: 'Pendant le glisser' },
]
</script>

<template>
  <div class="ombres-etats">
    <div
      v-for="({ etat, legende }, index) in ETATS"
      :key="etat"
      class="ombres-etats__etat"
    >
      <span class="ombres-etats__legende">{{ legende }}</span>
      <OmbresCarte
        :etat="etat"
        :candidature="CANDIDATURE"
        :card-index="index"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.ombres-etats {
  display: grid;
  grid-template-columns: repeat(2, var(--csp-kanban-column-width));
  place-content: center;
  gap: var(--csp-space-8) var(--csp-space-10);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--csp-region-background);
  color: var(--text-default-grey);
}

.ombres-etats__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ombres-etats__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
