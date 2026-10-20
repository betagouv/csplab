<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Encadre les commandes qui simulent l'action d'une autre personne (valideur, contributeur).
// Elles n'existeraient pas dans le produit : elles servent à faire avancer le scénario.
defineProps<{ titre?: string }>()
</script>

<template>
  <div class="simu">
    <span class="simu__label">
      <CspIcon
        name="ri:flask-line"
        :size="12"
      />
      {{ titre ?? 'Simulation' }}
    </span>
    <slot />
  </div>
</template>

<style scoped lang="scss">
.simu {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px dashed var(--border-plain-purple-glycine, #a558a0);
  background: var(--background-alt-purple-glycine, #fbf5fa);
}

.simu__label {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-label-purple-glycine, #6e445a);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
</style>
