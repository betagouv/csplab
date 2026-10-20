<script setup lang="ts">
import type { Candidature } from '@/features/candidatures/types'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'

export type OmbresEtat = 'repos' | 'survol' | 'focus' | 'glisser' | 'depose'

defineProps<{
  etat: OmbresEtat
  candidature: Candidature
  cardIndex: number
}>()
</script>

<template>
  <div :class="`ombres-carte ombres-carte--${etat}`">
    <CandidatureKanbanCard
      :candidature="candidature"
      board-id="ombres"
      column-id="ombres"
      :card-index="cardIndex"
    />
  </div>
</template>

<style scoped lang="scss">
/* Variables of the hover and drag states, set on an ancestor of a card that the pointer does not reach */
.ombres-carte--survol {
  --csp-raised-shadow: var(--csp-raised-shadow-hover, 0 1px 2px rgb(0 0 0 / 6%));
  --csp-raised-background: var(--csp-raised-background-hover, var(--background-alt-grey));
  --csp-raised-border-color: var(--csp-raised-border-color-hover, var(--border-default-grey));
}

.ombres-carte--glisser {
  --csp-raised-shadow: var(--csp-raised-shadow-drag, 0 1px 2px rgb(0 0 0 / 6%));

  opacity: var(--csp-raised-opacity-drag);
}

/* First frame of the animation of a card dropped in another column */
.ombres-carte--depose {
  --csp-raised-background: var(--csp-raised-background-drop);
}

/* The ring that the card draws when its link has the keyboard focus, which only one element of a page can hold */
.ombres-carte--focus :deep(.candidature-kanban-card) {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}
</style>
