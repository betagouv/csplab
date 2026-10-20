<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { ETAPES, useEtapes } from './useEtapes'

// Précédent / suivant. Pas de blocage : on peut avancer même s'il manque des informations.
const { aller, index } = useEtapes()
const precedent = computed(() => ETAPES[index.value - 1])
const suivant = computed(() => ETAPES[index.value + 1])
</script>

<template>
  <footer class="foot">
    <CspButton
      v-if="precedent"
      :label="precedent.libelle"
      variant="tertiary-no-outline"
      icon="ri:arrow-left-line"
      is-icon-left
      @click="aller(precedent.id)"
    />
    <span v-else />
    <CspButton
      v-if="suivant"
      :label="`Continuer : ${suivant.libelle.toLowerCase()}`"
      icon="ri:arrow-right-line"
      @click="aller(suivant.id)"
    />
  </footer>
</template>

<style scoped lang="scss">
.foot {
  display: flex;
  justify-content: space-between;
  gap: var(--csp-space-4);
}
</style>
