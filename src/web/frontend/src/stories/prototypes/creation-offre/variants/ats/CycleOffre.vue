<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Le cycle de vie de l'offre, avec la DAR comme étape conditionnelle.
const props = defineProps<{ offre: Offre }>()

const ORDRE = ['redaction', 'validation', 'a_publier', 'publiee', 'archivee'] as const
const etapes = computed(() => {
  const i = ORDRE.indexOf(props.offre.etat)
  const sansDar = props.offre.dar === 'non_requise'
  return [
    { id: 'redaction', label: 'Rédaction', detail: '' },
    { id: 'validation', label: 'Validation (DAR)', detail: sansDar ? 'Non requise par l\'organisme' : props.offre.darRef ?? '' },
    { id: 'a_publier', label: 'À publier', detail: 'Préparation' },
    { id: 'publiee', label: 'Publiée', detail: props.offre.publieeLe ?? '' },
    { id: 'archivee', label: 'Archivée', detail: '' },
  ].map((e, j) => ({
    ...e,
    etat: e.id === 'validation' && sansDar ? 'saute' : j < i ? 'fait' : j === i ? 'courant' : 'avenir',
  }))
})
</script>

<template>
  <ol
    class="cycle"
    aria-label="Cycle de vie de l'offre"
  >
    <li
      v-for="e in etapes"
      :key="e.id"
      class="cycle__etape"
      :class="`cycle__etape--${e.etat}`"
      :aria-current="e.etat === 'courant' ? 'step' : undefined"
    >
      <CspIcon
        :name="e.etat === 'fait' ? 'ri:checkbox-circle-fill' : e.etat === 'courant' ? 'ri:record-circle-fill' : e.etat === 'saute' ? 'ri:indeterminate-circle-line' : 'ri:checkbox-blank-circle-line'"
        :size="16"
      />
      <span>
        <strong>{{ e.label }}</strong>
        <small v-if="e.detail">{{ e.detail }}</small>
      </span>
    </li>
  </ol>
</template>

<style scoped lang="scss">
.cycle {
  display: flex;
  gap: var(--csp-space-2);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  list-style: none;
}

.cycle__etape {
  display: flex;
  flex: 1;
  align-items: flex-start;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
  }

  &--fait :deep(.csp-icon) {
    color: var(--text-default-success);
  }

  &--courant {
    color: var(--text-action-high-blue-france);
  }

  &--saute {
    opacity: 0.6;
  }
}
</style>
