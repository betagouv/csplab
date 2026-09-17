<script setup lang="ts">
defineEmits<{
  click: []
}>()
</script>

<template>
  <button
    type="button"
    class="fc-button"
    @click="$emit('click')"
  >
    <span class="fc-button__logo" aria-hidden="true">FC</span>
    <span class="fc-button__label">S'identifier avec FranceConnect</span>
  </button>
</template>

<style scoped lang="scss">
// Approximation du bouton officiel FranceConnect (composant non disponible côté DS) :
// mêmes proportions et logique de contraste que le bouton spec FranceConnect,
// avec les tokens de couleur du produit plutôt que la charte FranceConnect exacte.
.fc-button {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  width: 100%;
  min-height: 3rem;
  padding: var(--csp-space-2) var(--csp-space-4);
  border: none;
  border-radius: 0.25rem;
  background-color: #000091;
  color: #fff;
  cursor: pointer;
  font: inherit;
  font-weight: 600;
  font-size: 0.9375rem;

  &:hover {
    background-color: #1212ff;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.fc-button__logo {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.25rem;
  background-color: #fff;
  color: #000091;
  font-size: 0.75rem;
  font-weight: 800;
}

.fc-button__label {
  flex: 1;
  text-align: left;
}
</style>
