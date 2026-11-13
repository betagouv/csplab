<script setup lang="ts">
// Libellé + texte d'aide gris sous le libellé (modèle DSFR), pour les composants partagés qui n'ont pas
// d'aide (zone de texte, groupes de cases) : le composant glissé dedans garde son libellé, masqué à l'écran.
defineProps<{ label: string, hint?: string, forId?: string }>()
</script>

<template>
  <div class="champ">
    <component
      :is="forId ? 'label' : 'p'"
      :for="forId"
      class="champ__label"
    >
      {{ label }}
      <span
        v-if="hint"
        class="champ__hint"
      >{{ hint }}</span>
    </component>
    <div class="champ__controle">
      <slot />
    </div>
  </div>
</template>

<style scoped lang="scss">
.champ__label {
  display: flex;
  flex-direction: column;
  gap: var(--csp-field-hint-gap, 0.25rem);
  margin: 0 0 var(--csp-field-label-gap, 0.5rem);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.champ__hint {
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--text-mention-grey);
}

.champ__controle :deep(.csp-textarea-group__label),
.champ__controle :deep(.csp-textarea__label),
.champ__controle :deep(legend) {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
