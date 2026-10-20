<script setup lang="ts">
import FieldOrigin from './FieldOrigin.vue'

// Libellé de champ « maison » quand le composant Csp n'affiche pas lui-même son label
// (ou pour lui adjoindre l'origine de la valeur et la mention facultatif/obligatoire).
defineProps<{
  label: string
  forId?: string
  hint?: string
  path?: string
  requis?: boolean
  tag?: 'label' | 'span'
}>()
</script>

<template>
  <div class="field-label">
    <component
      :is="tag ?? 'label'"
      :for="tag === 'span' ? undefined : forId"
      class="field-label__text"
    >
      {{ label }}<span
        v-if="requis"
        class="field-label__req"
        aria-hidden="true"
      > *</span>
    </component>
    <FieldOrigin
      v-if="path"
      :path="path"
    />
  </div>
  <p
    v-if="hint"
    class="field-label__hint"
  >
    {{ hint }}
  </p>
</template>

<style scoped lang="scss">
.field-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-2);
  flex-wrap: wrap;
}

.field-label__text {
  font-size: var(--csp-font-size-base);
  color: var(--text-label-grey);
}

.field-label__req {
  color: var(--text-default-error);
}

.field-label__hint {
  margin: var(--csp-field-hint-gap, 0.25rem) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
