<script setup lang="ts">
import type { CandidatureEspace } from '../../data/espaceMock'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import StatutCandidatBadge from './StatutCandidatBadge.vue'

defineProps<{
  candidature: CandidatureEspace
  nonLus: number
}>()

defineEmits<{
  ouvrir: [id: string]
}>()
</script>

<template>
  <button
    type="button"
    class="carte"
    @click="$emit('ouvrir', candidature.id)"
  >
    <span class="carte__corps">
      <span class="carte__titre">
        <span
          v-if="nonLus > 0"
          class="carte__pastille"
          role="img"
          :aria-label="nonLus > 1 ? 'Nouveaux messages' : 'Nouveau message'"
        />
        <span class="carte__intitule">{{ candidature.intitule }}</span>
      </span>
      <span class="carte__organisme">{{ candidature.organisme }}</span>

      <span class="carte__statut">
        <StatutCandidatBadge :statut="candidature.statut" />
      </span>
      <span
        v-if="nonLus > 0"
        class="carte__etiquette"
      >
        {{ nonLus > 1 ? 'Nouveaux messages' : 'Nouveau message' }}
      </span>
    </span>

    <CspIcon
      name="ri:arrow-right-s-line"
      :size="22"
      class="carte__chevron"
    />
  </button>
</template>

<style scoped lang="scss">
.carte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  width: 100%;
  min-height: 3.5rem;
  padding: var(--csp-space-4);
  border: none;
  border-radius: 0.5rem;
  text-align: left;
  cursor: pointer;
  font: inherit;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);

  &:active {
    background-color: var(--background-alt-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.carte__corps {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
}

.carte__titre {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.carte__pastille {
  flex-shrink: 0;
  width: 0.75rem;
  height: 0.75rem;
  margin-top: 0.3125rem;
  border-radius: 50%;
  background-color: #0063cb;
}

.carte__intitule {
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text-title-grey);
}

.carte__organisme {
  font-size: 0.875rem;
  color: var(--text-default-grey);
}

.carte__statut {
  display: flex;
  margin-top: var(--csp-space-1);
}

.carte__etiquette {
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-size: 0.75rem;
  font-weight: 700;
}

.carte__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
