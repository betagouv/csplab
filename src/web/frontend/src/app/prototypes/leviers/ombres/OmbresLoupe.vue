<script setup lang="ts">
import type { Candidature } from '@/features/candidatures/types'
import OmbresCarte from './OmbresCarte.vue'

defineProps<{
  candidature: Candidature
}>()
</script>

<template>
  <div
    class="ombres-loupe"
    aria-hidden="true"
    inert
  >
    <OmbresCarte
      class="ombres-loupe__carte"
      etat="repos"
      :candidature="candidature"
    />
  </div>
</template>

<style scoped lang="scss">
/* The bottom right corner of the card at rest, four times larger, with room for the shadow: the card keeps its width,
   and its content stays hidden */
.ombres-loupe {
  position: relative;
  height: 7rem;
  overflow: hidden;
  background-color: var(--csp-region-background);
}

.ombres-loupe__carte {
  position: absolute;
  right: var(--csp-space-8);
  bottom: var(--csp-space-8);
  width: var(--csp-kanban-column-width);
  transform: scale(4);
  transform-origin: bottom right;
}

.ombres-loupe__carte :deep(.candidature-kanban-card > *) {
  visibility: hidden;
}
</style>
