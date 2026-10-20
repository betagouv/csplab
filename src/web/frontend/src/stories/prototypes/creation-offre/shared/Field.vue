<script setup lang="ts">
import FieldOrigin from './FieldOrigin.vue'

// Enveloppe d'un champ Csp* : affiche l'origine de la valeur (reprise / modifiée) à droite du libellé.
defineProps<{ path?: string }>()
</script>

<template>
  <div class="field">
    <FieldOrigin
      v-if="path"
      class="field__origin"
      :path="path"
    />
    <slot />
  </div>
</template>

<style scoped lang="scss">
.field {
  position: relative;
  min-width: 0;
}

.field__origin {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
}
</style>
