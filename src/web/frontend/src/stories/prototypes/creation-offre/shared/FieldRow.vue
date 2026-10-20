<script setup lang="ts">
// Ligne de formulaire : champ + indicateur d'origine aligné au-dessus à droite.
defineProps<{ path?: string, cols?: 1 | 2 | 3 }>()
</script>

<template>
  <div
    class="field-row"
    :class="cols ? `field-row--cols-${cols}` : undefined"
  >
    <slot />
  </div>
</template>

<style scoped lang="scss">
.field-row {
  display: grid;
  gap: var(--csp-space-5);

  &--cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  &--cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>
