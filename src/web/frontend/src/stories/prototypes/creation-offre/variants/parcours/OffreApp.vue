<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, StepId } from '../../data/types'
import { clone } from '../../data/scenario'
import { provideOffre } from '../../data/useOffre'
import OffreShell from '../../shared/OffreShell.vue'
import StepBesoin from '../../steps/StepBesoin.vue'
import StepConditions from '../../steps/StepConditions.vue'
import StepDemarrer from '../../steps/StepDemarrer.vue'
import StepDiffusion from '../../steps/StepDiffusion.vue'
import StepEvaluation from '../../steps/StepEvaluation.vue'
import StepOffre from '../../steps/StepOffre.vue'
import StepPoste from '../../steps/StepPoste.vue'
import StepRecap from '../../steps/StepRecap.vue'
import StepValidation from '../../steps/StepValidation.vue'

// Une offre en cours d'édition. Remontée (via :key) quand on reprend un autre brouillon ou qu'on duplique.
const props = defineProps<{ preset: Preset, init?: OffreState, initStep?: StepId }>()
const emit = defineEmits<{ reprendre: [preset: Preset], dupliquer: [state: OffreState] }>()

const store = provideOffre(props.preset)
if (props.init) {
  Object.assign(store.state, clone(props.init))
}
if (props.initStep) {
  store.step.value = props.initStep
}

const STEPS = {
  besoin: StepBesoin,
  poste: StepPoste,
  offre: StepOffre,
  conditions: StepConditions,
  evaluation: StepEvaluation,
  validation: StepValidation,
  diffusion: StepDiffusion,
}
</script>

<template>
  <OffreShell>
    <div
      v-if="store.reprise.value"
      class="reprise"
      role="status"
    >
      <strong>Reprise de l'offre {{ store.state.reference }}.</strong>
      <template v-if="store.state.statut === 'a_corriger'">
        Julien Lefèvre a demandé des corrections hier : elles sont listées ci-dessous et sur les étapes concernées.
      </template>
      <template v-else>
        Dernière modification il y a 3 jours. Il reste {{ store.manques.value.length }} information(s) requise(s) ; les étapes à compléter sont signalées à gauche.
      </template>
    </div>
    <StepDemarrer
      v-if="store.step.value === 'demarrer'"
      @reprendre="p => emit('reprendre', p)"
    />
    <StepRecap
      v-else-if="store.step.value === 'recap'"
      @dupliquer="emit('dupliquer', JSON.parse(JSON.stringify(store.state)))"
    />
    <component
      :is="STEPS[store.step.value]"
      v-else
    />
  </OffreShell>
</template>

<style scoped lang="scss">
.reprise {
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 4px solid var(--border-plain-info);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
}
</style>
