<script setup lang="ts">
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'

defineProps<{
  nomComplet: string
}>()

defineEmits<{
  accueil: []
  compte: []
}>()
</script>

<template>
  <header class="entete">
    <button
      type="button"
      class="entete__marque"
      aria-label="CSPLab — retour à mes candidatures"
      @click="$emit('accueil')"
    >
      <span class="entete__titre">CSPLab</span>
      <span class="entete__sous-titre">Espace candidat</span>
    </button>

    <div class="entete__actions">
      <button
        type="button"
        class="entete__compte"
        aria-label="Mon compte"
        @click="$emit('compte')"
      >
        <CspAvatar
          :name="nomComplet"
          size="sm"
        />
      </button>
    </div>
  </header>
</template>

<style scoped lang="scss">
.entete {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
  min-height: 3.5rem;
  padding: var(--csp-space-2) var(--csp-space-4);
  background-color: var(--background-default-grey);
  box-shadow: inset 0 -1px 0 var(--border-default-grey);
}

.entete__marque {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.1;
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-1) 0;
  min-height: 2.75rem;
  justify-content: center;
}

.entete__titre {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-action-high-blue-france);
}

.entete__sous-titre {
  margin-top: 0.125rem;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.entete__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.entete__compte {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.75rem;
  min-height: 2.75rem;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}
</style>
