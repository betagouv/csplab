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

// Les champs de l'annonce (ChampOffre) ont 4 px de moins entre libellé et champ que les champs du design system.
.field-row:is(.field-row--cols-2, .field-row--cols-3) :deep(.champ__tete:not(:has(+ .champ__hint))) {
  padding-bottom: 0.25rem;
}

// Sur une même ligne, un champ avec texte d'aide (« Facultatif ») et un champ sans : on réserve la place de l'aide
// sous les libellés qui n'en ont pas, pour que les champs restent alignés.
.field-row:is(.field-row--cols-2, .field-row--cols-3):has(
    .csp-input-group__hint,
    .csp-select-group__hint,
    .champ__hint
  ) {
  :deep(.csp-input-group__label:not(:has(.csp-input-group__hint))),
  :deep(.csp-select-group__label:not(:has(.csp-select-group__hint))) {
    padding-bottom: var(--reserve-aide, 1.375rem);
  }

  :deep(.champ__tete:not(:has(+ .champ__hint))) {
    padding-bottom: calc(var(--reserve-aide, 1.375rem) + 0.25rem);
  }
}
</style>
