<script setup lang="ts">
import type { CandidatureEspace } from '../../data/espaceMock'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formaterActivite } from '../../data/format'
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
    :class="{ 'carte--non-lus': nonLus > 0 }"
    @click="$emit('ouvrir', candidature.id)"
  >
    <span class="carte__corps">
      <span class="carte__intitule">{{ candidature.intitule }}</span>
      <span class="carte__organisme">{{ candidature.organisme }}</span>

      <span class="carte__statut">
        <StatutCandidatBadge :statut="candidature.statut" />
        <span
          v-if="nonLus > 0"
          class="carte__pastille"
          :aria-label="`${nonLus} message${nonLus > 1 ? 's' : ''} non lu${nonLus > 1 ? 's' : ''}`"
        >
          {{ nonLus }} non lu{{ nonLus > 1 ? 's' : '' }}
        </span>
      </span>

      <span class="carte__activite">
        Dernière activité : {{ formaterActivite(candidature.derniereActivite) }}
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

  &--non-lus {
    box-shadow:
      inset 0 0 0 1px var(--border-action-low-blue-france),
      inset 4px 0 0 var(--background-action-high-blue-france);
  }
}

.carte__corps {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
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
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-1);
}

.carte__pastille {
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-size: 0.75rem;
  font-weight: 700;
}

.carte__activite {
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.carte__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
