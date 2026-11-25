<script setup lang="ts">
import { computed } from 'vue'

// Texte où l'astérisque des champs obligatoires s'affiche en rouge, comme dans les libellés des champs.
const props = defineProps<{ texte: string }>()
const morceaux = computed(() => props.texte.split('*'))
</script>

<template>
  <span><template
    v-for="(m, i) in morceaux"
    :key="i"
  >{{ m }}<abbr
    v-if="i < morceaux.length - 1"
    class="etoile"
    title="obligatoire"
  >*</abbr></template></span>
</template>

<style scoped lang="scss">
.etoile {
  color: var(--text-default-error);
  text-decoration: none;
}
</style>
