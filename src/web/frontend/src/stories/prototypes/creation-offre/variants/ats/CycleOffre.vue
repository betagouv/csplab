<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import { db } from './store'

// Où en est l'offre, d'après la maquette d'Alice : barre segmentée dans un cadre, purement informative.
// Étapes passées et en cours en bleu (l'étape en cours en gras), étapes à venir en gris.
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
const courante = computed(() => etapes.value.find(e => e.etat === 'courant'))
</script>

<template>
  <div
    class="cycle"
    role="img"
    :aria-label="`Étape de l'offre : ${courante?.label ?? ''}${courante?.detail ? `, ${courante.detail}` : ''}`"
  >
    <div
      v-for="e in etapes"
      :key="e.id"
      class="cycle__etape"
      :class="`cycle__etape--${e.etat}`"
      aria-hidden="true"
    >
      <span class="cycle__barre" />
      <span class="cycle__texte">
        {{ e.label }}<template v-if="e.detail"> • {{ e.detail }}</template>
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.cycle {
  display: flex;
  gap: 3px;
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  cursor: default;
  user-select: none;
}

.cycle__etape {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-2);
  min-width: 0;
  text-align: center;

  &:first-child {
    text-align: left;
  }

  &:last-child {
    text-align: right;
  }
}

.cycle__barre {
  height: 4px;
  background: var(--background-contrast-grey);

  .cycle__etape--fait &,
  .cycle__etape--courant & {
    background: var(--background-action-high-blue-france);
  }
}

.cycle__texte {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);

  .cycle__etape--fait & {
    color: var(--text-action-high-blue-france);
  }

  .cycle__etape--courant & {
    color: var(--text-action-high-blue-france);
    font-weight: var(--csp-font-weight-bold);
  }
}
</style>
