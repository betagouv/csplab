<script setup lang="ts">
import type { ReponsesQualification } from '../../shared/QuestionsQualification.vue'
import { computed, reactive, ref } from 'vue'
import { offrePrincipale } from '../../data/candidatMock'
import CandidatureFlowShell from '../../shared/CandidatureFlowShell.vue'
import FileDropzone from '../../shared/FileDropzone.vue'
import QuestionsQualification from '../../shared/QuestionsQualification.vue'
import SuccesAvecCompte from '../succes/SuccesAvecCompte.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'

const offre = offrePrincipale
const steps = ['Compte', 'Informations', 'CV', 'Questions', 'Récapitulatif', 'Envoyée']
const currentIndex = ref(0)

const compte = reactive({ email: '', motDePasse: '' })
const infos = reactive({ prenom: '', nom: '', telephone: '' })
const cvFileName = ref<string | null>(null)
const reponses = ref<ReponsesQualification>({ titulaireFp: '', disponibleSeptembre: '', permisB: '' })

const isLastContentStep = computed(() => currentIndex.value === 4)
const nextDisabled = computed(() => {
  if (currentIndex.value === 0) {
    return !compte.email || !compte.motDePasse
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
  <SuccesAvecCompte v-if="currentIndex === 5" />

  <CandidatureFlowShell
    v-else
    :steps="steps"
    :current-index="currentIndex"
    :is-last-content-step="isLastContentStep"
    :next-disabled="nextDisabled"
    :show-account-hint="false"
    @back="back"
    @next="next"
  >
    <template v-if="currentIndex === 0">
      <h1 class="step-title">
        Créez votre compte
      </h1>
      <p class="step-hint">
        Vous pourrez retrouver toutes vos candidatures et vos échanges avec les recruteurs
        dans un même espace.
      </p>
      <CspInput
        v-model="compte.email"
        type="email"
        label="Adresse email"
      />
      <CspInput
        v-model="compte.motDePasse"
        type="password"
        label="Mot de passe"
      />
    </template>

    <template v-else-if="currentIndex === 1">
      <h1 class="step-title">
        Vos informations
      </h1>
      <CspInput
        v-model="infos.prenom"
        label="Prénom"
      />
      <CspInput
        v-model="infos.nom"
        label="Nom"
      />
      <CspInput
        v-model="infos.telephone"
        type="tel"
        label="Téléphone"
      />
    </template>

    <template v-else-if="currentIndex === 2">
      <h1 class="step-title">
        Ajoutez votre CV
      </h1>
      <p class="step-hint">
        Pour l'offre <strong>{{ offre.intitule }}</strong> — {{ offre.organisme }}.
      </p>
      <FileDropzone
        :file-name="cvFileName"
        @select="(name) => cvFileName = name"
        @remove="cvFileName = null"
      />
    </template>

    <template v-else-if="currentIndex === 3">
      <h1 class="step-title">
        Quelques questions
      </h1>
      <QuestionsQualification v-model="reponses" />
    </template>

    <template v-else-if="currentIndex === 4">
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
          <dt>Compte</dt>
          <dd>{{ compte.email }}</dd>
        </div>
        <div class="recap__row">
          <dt>CV</dt>
          <dd>{{ cvFileName }}</dd>
        </div>
        <div class="recap__row">
          <dt>Candidat</dt>
          <dd>{{ infos.prenom }} {{ infos.nom }}</dd>
        </div>
      </dl>

      <CspCallout
        variant="info"
        title="Après l'envoi"
        description="Vous retrouverez cette candidature dans votre espace personnel, avec son suivi en temps réel."
      />
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
