<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Encadré gris qui regroupe, au sein d'un bloc de l'annonce, les informations de suivi interne :
// jamais publiées, jamais reprises d'une fiche ni d'une offre dupliquée.
</script>

<template>
  <div
    class="suivi"
    role="group"
    aria-label="Suivi interne, non publié"
  >
    <p class="suivi__tete">
      <CspIcon
        name="ri:lock-line"
        :size="14"
      />
      Suivi interne · non publié
    </p>
    <slot />
  </div>
</template>

<style scoped lang="scss">
.suivi {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4);
  border-left: 3px solid var(--border-plain-grey);
  background: var(--background-alt-grey);
}

.suivi__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-mention-grey);
}
</style>
