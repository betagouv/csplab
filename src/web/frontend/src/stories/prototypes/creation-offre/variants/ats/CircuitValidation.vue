<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import SimulationNote from '../../shared/SimulationNote.vue'
import { useNav } from './nav'
import { decider, le, peutDecider } from './store'

// Circuit de validation d'une offre : valideurs définis par le superviseur, l'un après l'autre ou en parallèle.
// Les décisions des valideurs sont simulées (encadré violet).
const props = defineProps<{ offre: Offre }>()
const { notifier } = useNav()
const o = computed(() => props.offre)

const etapes = computed(() => (o.value.validations ?? []).map((v, i) => ({
  ...v,
  i,
  actif: peutDecider(o.value, i),
})))

const refusEn = ref<number | null>(null)
const motif = ref('Merci de préciser le motif du recrutement et le poste remplacé.')

function valider(i: number) {
  const nom = o.value.validations![i]!.nom
  decider(o.value, i, 'validee')
  notifier(o.value.etat === 'a_publier'
    ? 'Validation terminée (simulation). L\'offre peut être relue puis publiée.'
    : `Validée par ${nom} (simulation). En attente des autres valideurs.`)
}
function refuser(i: number) {
  decider(o.value, i, 'refusee', motif.value)
  refusEn.value = null
  notifier('Offre refusée (simulation) : elle redevient modifiable.')
}

function icone(d: string, actif: boolean) {
  if (d === 'validee') {
    return 'ri:checkbox-circle-fill'
  }
  if (d === 'refusee') {
    return 'ri:error-warning-line'
  }
  return actif ? 'ri:record-circle-fill' : 'ri:checkbox-blank-circle-line'
}
function statut(d: string, actif: boolean, quand?: string) {
  if (d === 'validee') {
    return `Validée ${le(quand)}`
  }
  if (d === 'refusee') {
    return `Refusée ${le(quand)}`
  }
  return actif ? 'Décision attendue' : 'En attente du valideur précédent'
}
</script>

<template>
  <div class="circuit">
    <p class="circuit__mode">
      {{ o.circuit === 'simultane' ? 'Tous les valideurs en parallèle' : 'Les valideurs l\'un après l\'autre' }} · {{ o.darRef }}
    </p>
    <ol class="circuit__liste">
      <li
        v-for="e in etapes"
        :key="e.i"
        class="etape"
        :class="`etape--${e.decision}`"
      >
        <CspIcon
          :name="icone(e.decision, e.actif)"
          :size="16"
        />
        <span>
          <strong>{{ e.nom }}</strong>
          <small>{{ e.fonction }} — {{ statut(e.decision, e.actif, e.le) }}</small>
          <small v-if="e.motif">« {{ e.motif }} »</small>
        </span>
      </li>
    </ol>

    <template
      v-for="e in etapes"
      :key="`sim-${e.i}`"
    >
      <SimulationNote
        v-if="e.actif"
        :titre="`Décision de ${e.nom}`"
      >
        <CspButton
          label="Valider"
          size="sm"
          @click="valider(e.i)"
        />
        <CspButton
          label="Refuser"
          size="sm"
          variant="secondary"
          @click="refusEn = refusEn === e.i ? null : e.i"
        />
      </SimulationNote>
      <template v-if="refusEn === e.i">
        <CspTextarea
          v-model="motif"
          label="Motif du refus"
          :rows="3"
        />
        <div>
          <CspButton
            label="Envoyer le refus"
            size="sm"
            @click="refuser(e.i)"
          />
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped lang="scss">
.circuit {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.circuit__mode {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.circuit__liste {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.etape {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &--validee :deep(.csp-icon) {
    color: var(--text-default-success);
  }

  &--refusee :deep(.csp-icon) {
    color: var(--text-default-warning);
  }

  &--attente :deep(.csp-icon) {
    color: var(--text-action-high-blue-france);
  }
}
</style>
