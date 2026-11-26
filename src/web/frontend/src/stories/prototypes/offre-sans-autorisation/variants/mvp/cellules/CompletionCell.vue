<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { champsObligatoires } from '../aide'

// « Champs obligatoires remplis » (onglet En préparation, retour PO 26/11/2026) : explique pourquoi une offre
// est encore en brouillon ou déjà prête à publier.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const champs = computed(() => champsObligatoires(props.row))
const remplis = computed(() => champs.value.filter(c => c.ok).length)
const complet = computed(() => remplis.value === champs.value.length)
</script>

<template>
  <div
    class="completion"
    :class="{ 'completion--ok': complet }"
  >
    <span class="completion__texte">{{ remplis }} / {{ champs.length }}</span>
    <span
      class="completion__jauge"
      aria-hidden="true"
    >
      <span :style="{ width: `${(remplis / Math.max(1, champs.length)) * 100}%` }" />
    </span>
  </div>
</template>

<style scoped lang="scss">
.completion {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 7rem;
}

.completion__texte {
  white-space: nowrap;
}

.completion__jauge {
  display: block;
  height: 4px;
  background: var(--background-contrast-grey);

  span {
    display: block;
    height: 100%;
    background: var(--background-action-high-blue-france);
  }
}

.completion--ok .completion__jauge span {
  background: var(--background-flat-success);
}
</style>
