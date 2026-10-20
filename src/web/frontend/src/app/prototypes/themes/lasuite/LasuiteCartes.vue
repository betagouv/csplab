<script setup lang="ts">
import { DEMO_CANDIDATURE } from '@/api/__mocks__/demo'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'

// The story opens the panel of DEMO_CANDIDATURE: its card is the open one
const CANDIDATURES = demoKanban().etapes[0]!.candidatures
const AUTRE = CANDIDATURES.find(({ uuid }) => uuid !== DEMO_CANDIDATURE.uuid)!
const OUVERTE = CANDIDATURES.find(({ uuid }) => uuid === DEMO_CANDIDATURE.uuid)!

const ETATS = [
  { id: 'repos', legende: 'Au repos', candidature: AUTRE },
  { id: 'survol', legende: 'Au survol', candidature: AUTRE },
  { id: 'focus', legende: 'Focus clavier', candidature: AUTRE },
  { id: 'ouverte', legende: 'Ouverte', candidature: OUVERTE },
  { id: 'glisser', legende: 'Pendant le glisser', candidature: AUTRE },
  { id: 'deposee', legende: 'Déposée', candidature: AUTRE },
] as const
</script>

<template>
  <div class="lasuite-cartes">
    <div class="lasuite-cartes__grille">
      <figure
        v-for="(etat, index) in ETATS"
        :key="etat.id"
        class="lasuite-cartes__etat"
      >
        <figcaption class="lasuite-cartes__legende">
          {{ etat.legende }}
        </figcaption>
        <div :class="`lasuite-cartes__carte lasuite-cartes__carte--${etat.id}`">
          <CandidatureKanbanCard
            :candidature="etat.candidature"
            board-id="lasuite-cartes"
            :column-id="`lasuite-cartes-${index}`"
          />
        </div>
      </figure>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* Six cards on the background of a kanban column, enlarged for a slide */
.lasuite-cartes {
  display: grid;
  place-content: center;
  height: 100vh;
  background-color: var(--csp-region-background);
  color: var(--text-default-grey);
}

.lasuite-cartes__grille {
  display: grid;
  grid-template-columns: repeat(3, var(--csp-kanban-column-width));
  gap: var(--csp-space-6) var(--csp-space-8);
  zoom: 1.25;
}

.lasuite-cartes__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
}

.lasuite-cartes__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

/* Variables of the hover and drag states, set on an ancestor of a card that the pointer does not reach */
.lasuite-cartes__carte--survol {
  --csp-raised-shadow: var(--csp-raised-shadow-hover);
  --csp-raised-background: var(--csp-raised-background-hover);
}

.lasuite-cartes__carte--glisser {
  --csp-raised-shadow: var(--csp-raised-shadow-drag);

  opacity: var(--csp-raised-opacity-drag);
}

/* The ring that the card draws when its link has the keyboard focus, which only one element of a page can hold */
.lasuite-cartes__carte--focus :deep(.candidature-kanban-card) {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}

/* The first frame of the animation of a dropped card */
.lasuite-cartes__carte--deposee :deep(.candidature-kanban-card) {
  outline: 2px solid var(--csp-raised-outline-color-drop);
  outline-offset: -2px;
}
</style>
