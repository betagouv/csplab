<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Structure de champ DSFR pour les composants partagés qui ne l'offrent pas entièrement :
// libellé, texte d'aide gris sous le libellé (ex. « Champ obligatoire »), le champ, puis un message
// d'information sous le champ (icône bleue). Le composant glissé dedans garde son libellé, masqué à l'écran
// quand ce cadre affiche le sien.
defineProps<{ label?: string, hint?: string, forId?: string, info?: string }>()
</script>

<template>
  <div class="champ">
    <component
      :is="forId ? 'label' : 'p'"
      v-if="label"
      :for="forId"
      class="champ__label"
    >
      {{ label }}
      <span
        v-if="hint"
        class="champ__hint"
      >{{ hint }}</span>
    </component>
    <div :class="{ champ__controle: label }">
      <slot />
    </div>
    <p
      v-if="info"
      class="champ__info"
    >
      <CspIcon
        name="ri:information-fill"
        :size="16"
      />
      {{ info }}
    </p>
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

.champ__info {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-1);
  margin: var(--csp-space-2) 0 0;
  font-size: 0.75rem;
  color: var(--text-default-info);

  :deep(svg) {
    flex-shrink: 0;
  }
}

.champ__controle :deep(.csp-textarea-group__label),
.champ__controle :deep(legend) {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
