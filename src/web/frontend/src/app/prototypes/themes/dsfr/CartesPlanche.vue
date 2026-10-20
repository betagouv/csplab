<script setup lang="ts">
import type { Candidature } from '@/features/candidatures/types'
import { DEMO_CANDIDATURE } from '@/api/__mocks__/demo'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'

type Etat = 'repos' | 'survol' | 'focus' | 'ouverte' | 'deposee' | 'glisser'

const CANDIDATURES = demoKanban().etapes.flatMap(etape => etape.candidatures)
// The open card is the candidature of the route of the story, which the panel shows
const OUVERTE = CANDIDATURES.find(({ uuid }) => uuid === DEMO_CANDIDATURE.uuid)!
const AUTRES = CANDIDATURES.filter(candidature => candidature !== OUVERTE)

const ETATS: { etat: Etat, legende: string, candidature: Candidature }[] = [
  { etat: 'repos', legende: 'Au repos', candidature: AUTRES[0]! },
  { etat: 'survol', legende: 'Au survol', candidature: AUTRES[0]! },
  { etat: 'focus', legende: 'Focus clavier', candidature: AUTRES[0]! },
  { etat: 'ouverte', legende: 'Ouverte dans le panneau', candidature: OUVERTE },
  { etat: 'deposee', legende: 'Déposée dans une autre étape', candidature: AUTRES[1]! },
  { etat: 'glisser', legende: 'Pendant le glisser', candidature: AUTRES[1]! },
]
</script>

<template>
  <div class="cartes-planche">
    <div
      v-for="({ etat, legende, candidature }, index) in ETATS"
      :key="etat"
      class="cartes-planche__etat"
    >
      <span class="cartes-planche__legende">{{ legende }}</span>
      <div :class="`cartes-planche__carte cartes-planche__carte--${etat}`">
        <CandidatureKanbanCard
          :candidature="candidature"
          board-id="cartes"
          :column-id="`cartes-${index}`"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.cartes-planche {
  display: grid;
  grid-template-columns: repeat(3, var(--csp-kanban-column-width));
  place-content: center;
  align-items: start;
  gap: var(--csp-space-8) var(--csp-space-10);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--csp-region-background);
  color: var(--text-default-grey);
}

.cartes-planche__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.cartes-planche__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

/* Variables of the hover and drag states, set on an ancestor of a card that the pointer does not reach */
.cartes-planche__carte--survol {
  --csp-raised-shadow: var(--csp-raised-shadow-hover);
  --csp-raised-background: var(--csp-raised-background-hover);
  --csp-raised-border-color: var(--csp-raised-border-color-hover, var(--border-default-grey));
}

.cartes-planche__carte--glisser {
  --csp-raised-shadow: var(--csp-raised-shadow-drag);

  opacity: var(--csp-raised-opacity-drag);
}

/* The ring that the card draws when its link has the keyboard focus */
.cartes-planche__carte--focus :deep(.candidature-kanban-card) {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}

/* The first image of the outline that fades out on a card dropped in another step */
.cartes-planche__carte--deposee :deep(.candidature-kanban-card) {
  outline: 2px solid var(--csp-raised-outline-color-drop);
  outline-offset: -2px;
}
</style>
