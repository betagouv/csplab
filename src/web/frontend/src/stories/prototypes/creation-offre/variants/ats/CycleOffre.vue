<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import { db } from './store'

// Où en est l'offre : repère visuel et informatif, rien n'y est cliquable.
// La validation n'apparaît que si l'organisme l'a activée (ou si elle a été demandée).
const props = defineProps<{ offre: Offre }>()

const etapes = computed(() => {
  const o = props.offre
  const avecValidation = db.organisme.validationActive || o.validationEtat !== 'non_demandee'
  const rang = { brouillon: 0, publiee: 2, retiree: 3, archivee: 4 }[o.etat]
  const validation = avecValidation
    ? [{ id: 'validation', label: 'Validation', detail: { non_demandee: 'à demander', en_attente: 'en attente', validee: 'obtenue', refusee: 'refusée' }[o.validationEtat], fait: rang > 0, courant: o.etat === 'brouillon' && o.validationEtat !== 'non_demandee' }]
    : []
  return [
    { id: 'brouillon', label: 'Brouillon', detail: '', fait: rang > 0 || (avecValidation && o.validationEtat !== 'non_demandee'), courant: o.etat === 'brouillon' && (!avecValidation || o.validationEtat === 'non_demandee') },
    ...validation,
    { id: 'publiee', label: 'Publiée', detail: o.dateFin && o.etat === 'publiee' ? `jusqu'au ${o.dateFin.split('-').reverse().join('/')}` : '', fait: rang > 2, courant: rang === 2 },
    { id: 'retiree', label: 'Retirée', detail: '', fait: rang > 3, courant: rang === 3 },
    { id: 'archivee', label: 'Archivée', detail: '', fait: false, courant: rang === 4 },
  ].map(e => ({ ...e, etat: e.courant ? 'courant' : e.fait ? 'fait' : 'avenir' }))
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
