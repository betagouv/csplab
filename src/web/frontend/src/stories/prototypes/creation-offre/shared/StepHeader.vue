<script setup lang="ts">
import type { StepId } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import { personne } from '../data/referentiels'
import { STEPS, useOffre } from '../data/useOffre'

// En-tête d'étape : titre, intention, informations manquantes, remarques des valideurs
// et verrouillage quand l'offre est en validation ou validée.
const props = defineProps<{ id: StepId, description: string }>()

const { state, manquesDe, verrouille, retirerDeValidation, modifierApresValidation } = useOffre()
const def = computed(() => STEPS.find(s => s.id === props.id)!)
const manques = computed(() => manquesDe(props.id))
const remarques = computed(() => state.remarques.filter(r => r.stepId === props.id && !r.resolue))
</script>

<template>
  <header class="step-header">
    <p class="step-header__phase">
      {{ def.phase }}
    </p>
    <h2 class="step-header__title">
      {{ def.libelle }}
    </h2>
    <p class="step-header__desc">
      {{ description }}
    </p>

    <CspCallout
      v-for="r in remarques"
      :key="r.id"
      variant="error"
      :title="`Correction demandée par ${personne(r.auteurId).nom}`"
    >
      <p class="step-header__remark">
        « {{ r.texte }} »
      </p>
      <CspButton
        label="Marquer comme traitée"
        variant="secondary"
        size="sm"
        icon="ri:check-line"
        is-icon-left
        @click="r.resolue = true"
      />
    </CspCallout>

    <CspCallout
      v-if="verrouille && state.statut === 'a_valider' && id !== 'validation'"
      variant="info"
      title="Offre en cours de validation — lecture seule"
    >
      <p class="step-header__remark">
        Pour modifier le contenu, retirez l'offre du circuit. Les valideurs en seront informés.
      </p>
      <CspButton
        label="Retirer de la validation pour modifier"
        variant="secondary"
        size="sm"
        @click="retirerDeValidation"
      />
    </CspCallout>
    <CspCallout
      v-else-if="verrouille && state.statut === 'validee' && id !== 'validation'"
      variant="success"
      title="Offre validée — lecture seule"
    >
      <p class="step-header__remark">
        Toute modification renverra l'offre en validation (hypothèse : à confirmer selon les organisations).
      </p>
      <CspButton
        label="Modifier quand même"
        variant="secondary"
        size="sm"
        @click="modifierApresValidation"
      />
    </CspCallout>

    <div
      v-if="manques.length && !verrouille"
      class="step-header__missing"
      role="status"
    >
      <strong>{{ manques.length }} information{{ manques.length > 1 ? 's' : '' }} requise{{ manques.length > 1 ? 's' : '' }} :</strong>
      {{ manques.map(m => m.libelle).join(' · ') }}
    </div>
  </header>
</template>

<style scoped lang="scss">
.step-header {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.step-header__phase {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-mention-grey);
}

.step-header__title {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-2xl);
  line-height: var(--csp-line-height-tight);
}

.step-header__desc {
  margin: 0;
  max-width: 48rem;
  color: var(--text-mention-grey);
}

.step-header__remark {
  margin: 0 0 var(--csp-space-2);
}

.step-header__missing {
  padding: var(--csp-space-2) var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
  background: var(--background-contrast-warning);
  color: var(--text-default-grey);
}
</style>
