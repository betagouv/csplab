<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'

// Où en est l'offre : repère visuel et informatif, rien n'y est cliquable. La validation est conditionnelle (DAR).
const props = defineProps<{ offre: Offre }>()

const ORDRE = ['redaction', 'validation', 'a_publier', 'publiee', 'archivee'] as const
const etapes = computed(() => {
  const i = ORDRE.indexOf(props.offre.etat)
  const sansDar = props.offre.dar === 'non_requise'
  return [
    { id: 'redaction', label: 'Brouillon', detail: '' },
    { id: 'validation', label: 'Validation', detail: sansDar ? 'Non requise par l\'organisme' : props.offre.validations ? `${props.offre.validations.filter(v => v.decision === 'validee').length}/${props.offre.validations.length} valideurs` : '' },
    { id: 'a_publier', label: 'À publier', detail: 'Relecture' },
    { id: 'publiee', label: 'Publiée', detail: props.offre.publieeLe ?? '' },
    { id: 'archivee', label: 'Archivée', detail: '' },
  ].map((e, j) => ({
    ...e,
    etat: e.id === 'validation' && sansDar ? 'saute' : j < i ? 'fait' : j === i ? 'courant' : 'avenir',
  }))
})
</script>

<template>
  <div
    class="cycle"
    role="img"
    :aria-label="`Étape de l'offre : ${etapes.find(e => e.etat === 'courant')?.label ?? ''}`"
  >
    <template
      v-for="(e, i) in etapes"
      :key="e.id"
    >
      <span
        v-if="i > 0"
        class="cycle__trait"
        :class="{ 'cycle__trait--fait': e.etat === 'fait' || e.etat === 'courant' }"
        aria-hidden="true"
      />
      <span
        class="cycle__etape"
        :class="`cycle__etape--${e.etat}`"
        aria-hidden="true"
      >
        <span class="cycle__point" />
        <span class="cycle__texte">
          {{ e.label }}<template v-if="e.detail"> · {{ e.detail }}</template>
        </span>
      </span>
    </template>
  </div>
</template>

<style scoped lang="scss">
.cycle {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  cursor: default;
  user-select: none;
}

.cycle__etape {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  white-space: nowrap;

  &--courant {
    color: var(--text-default-grey);
    font-weight: var(--csp-font-weight-bold);
  }

  &--saute {
    text-decoration: line-through;
    opacity: 0.6;
  }
}

.cycle__point {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--border-default-grey);

  .cycle__etape--fait & {
    background: var(--text-mention-grey);
  }

  .cycle__etape--courant & {
    width: 0.625rem;
    height: 0.625rem;
    background: var(--text-default-grey);
  }
}

.cycle__trait {
  flex: 1;
  max-width: 4rem;
  height: 1px;
  background: var(--border-default-grey);

  &--fait {
    background: var(--text-mention-grey);
  }
}
</style>
