<script setup lang="ts">
import type { StepId } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { STEPS, useOffre } from '../data/useOffre'

// Pied d'étape : précédent / suivant. L'enregistrement est dans la barre du haut, toujours visible.
const props = defineProps<{ id: StepId }>()
const { aller } = useOffre()

const index = computed(() => STEPS.findIndex(s => s.id === props.id))
const precedent = computed(() => STEPS[index.value - 1])
const suivant = computed(() => STEPS[index.value + 1])
</script>

<template>
  <footer class="step-footer">
    <CspButton
      v-if="precedent"
      :label="precedent.libelle"
      variant="tertiary"
      icon="ri:arrow-left-line"
      is-icon-left
      @click="aller(precedent.id)"
    />
    <span v-else />
    <CspButton
      v-if="suivant"
      :label="`Continuer : ${suivant.libelle}`"
      icon="ri:arrow-right-line"
      @click="aller(suivant.id)"
    />
  </footer>
</template>

<style scoped lang="scss">
.step-footer {
  display: flex;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding-top: var(--csp-space-5);
  border-top: 1px solid var(--border-default-grey);
}
</style>
