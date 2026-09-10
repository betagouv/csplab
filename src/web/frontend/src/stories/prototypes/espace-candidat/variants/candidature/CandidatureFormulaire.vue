<script setup lang="ts">
import type { ReponsesQualification } from '../../shared/QuestionsQualification.vue'
import { computed, reactive, ref } from 'vue'
import { offrePrincipale } from '../../data/candidatMock'
import CandidatureFlowShell from '../../shared/CandidatureFlowShell.vue'
import QuestionsQualification from '../../shared/QuestionsQualification.vue'
import SuccesSansCompte from '../succes/SuccesSansCompte.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const offre = offrePrincipale
const steps = ['Formulaire', 'Questions', 'Récapitulatif', 'Envoyée']
const currentIndex = ref(0)

const infos = reactive({
  prenom: '',
  nom: '',
  email: '',
  telephone: '',
  adresse: '',
  disponibilite: '',
  motivation: '',
})
const reponses = ref<ReponsesQualification>({ titulaireFp: '', disponibleSeptembre: '', permisB: '' })

const disponibiliteOptions = [
  { value: 'immediate', label: 'Immédiate' },
  { value: '1-mois', label: 'Sous 1 mois' },
  { value: '3-mois', label: 'Sous 3 mois' },
]

const isLastContentStep = computed(() => currentIndex.value === 2)
const nextDisabled = computed(() => {
  if (currentIndex.value === 0) {
    return !infos.prenom || !infos.nom || !infos.email
  }
  return false
})

function next() {
  currentIndex.value += 1
}

function back() {
  currentIndex.value -= 1
}
</script>

<template>
  <SuccesSansCompte v-if="currentIndex === 3" />

  <CandidatureFlowShell
    v-else
    :steps="steps"
    :current-index="currentIndex"
    :is-last-content-step="isLastContentStep"
    :next-disabled="nextDisabled"
    @back="back"
    @next="next"
  >
    <template v-if="currentIndex === 0">
      <h1 class="step-title">
        Vos informations
      </h1>
      <p class="step-hint">
        Pour l'offre <strong>{{ offre.intitule }}</strong> — {{ offre.organisme }}.
      </p>
      <CspInput
        v-model="infos.prenom"
        label="Prénom"
      />
      <CspInput
        v-model="infos.nom"
        label="Nom"
      />
      <CspInput
        v-model="infos.email"
        type="email"
        label="Adresse email"
      />
      <CspInput
        v-model="infos.telephone"
        type="tel"
        label="Téléphone"
      />
      <CspInput
        v-model="infos.adresse"
        label="Adresse postale"
      />
      <CspSelect
        v-model="infos.disponibilite"
        label="Disponibilité"
        placeholder="Sélectionnez une option"
        :options="disponibiliteOptions"
      />
      <CspTextarea
        v-model="infos.motivation"
        label="Lettre de motivation (facultatif)"
        :rows="4"
      />
    </template>

    <template v-else-if="currentIndex === 1">
      <h1 class="step-title">
        Quelques questions
      </h1>
      <QuestionsQualification v-model="reponses" />
    </template>

    <template v-else-if="currentIndex === 2">
      <h1 class="step-title">
        Vérifiez votre candidature
      </h1>
      <p class="step-hint">
        Dernière vérification avant l'envoi.
      </p>

      <dl class="recap">
        <div class="recap__row">
          <dt>Offre</dt>
          <dd>{{ offre.intitule }} — {{ offre.organisme }}</dd>
        </div>
        <div class="recap__row">
          <dt>Candidat</dt>
          <dd>{{ infos.prenom }} {{ infos.nom }} — {{ infos.email }}</dd>
        </div>
        <div class="recap__row">
          <dt>Disponibilité</dt>
          <dd>{{ disponibiliteOptions.find(o => o.value === infos.disponibilite)?.label ?? 'Non renseignée' }}</dd>
        </div>
      </dl>
    </template>
  </CandidatureFlowShell>
</template>

<style scoped lang="scss">
.step-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.step-hint {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
  line-height: 1.5;
}

.recap {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
}

.recap__row {
  padding-bottom: var(--csp-space-3);
  border-bottom: 1px solid var(--border-default-grey);

  &:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  dt {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: var(--text-mention-grey);
    margin: 0 0 0.125rem;
  }

  dd {
    margin: 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: var(--text-default-grey);
  }
}
</style>
