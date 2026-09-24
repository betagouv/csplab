<script setup lang="ts">
import type { ReponsesQualification } from '../../shared/QuestionsQualification.vue'
import { computed, reactive, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { offrePrincipale } from '../../data/candidatMock'
import CandidatureFlowShell from '../../shared/CandidatureFlowShell.vue'
import FileDropzone from '../../shared/FileDropzone.vue'
import QuestionsQualification from '../../shared/QuestionsQualification.vue'

const offre = offrePrincipale
const steps = ['Informations', 'Pièces jointes', 'Questions', 'Récapitulatif']
const currentIndex = ref(0)
const succesOuvert = ref(false)

const infos = reactive({ prenom: '', nom: '', email: '', telephone: '' })
const cvFileName = ref<string | null>(null)
const lettreFileName = ref<string | null>(null)
const reponses = ref<ReponsesQualification>({ titulaireFp: '', disponibleSeptembre: '', permisB: '' })

const isLastContentStep = computed(() => currentIndex.value === steps.length - 1)

const nextDisabled = computed(() => {
  if (currentIndex.value === 0) {
    return !infos.prenom || !infos.nom || !infos.email
  }
  if (currentIndex.value === 1) {
    return !cvFileName.value
  }
  return false
})

function next() {
  if (isLastContentStep.value) {
    succesOuvert.value = true
    return
  }
  currentIndex.value += 1
}

function back() {
  currentIndex.value -= 1
}
</script>

<template>
  <CandidatureFlowShell
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
    </template>

    <template v-else-if="currentIndex === 1">
      <h1 class="step-title">
        Pièces jointes
      </h1>
      <div class="piece">
        <p class="piece__label">
          CV <span class="piece__requis">(obligatoire)</span>
        </p>
        <FileDropzone
          :file-name="cvFileName"
          @select="(name) => cvFileName = name"
          @remove="cvFileName = null"
        />
      </div>
      <div class="piece">
        <p class="piece__label">
          Lettre de motivation <span class="piece__optionnel">(facultative, sauf si l'organisme la demande)</span>
        </p>
        <FileDropzone
          label="Déposez votre lettre de motivation, ou"
          :file-name="lettreFileName"
          @select="(name) => lettreFileName = name"
          @remove="lettreFileName = null"
        />
      </div>
    </template>

    <template v-else-if="currentIndex === 2">
      <h1 class="step-title">
        Quelques questions
      </h1>
      <QuestionsQualification v-model="reponses" />
    </template>

    <template v-else-if="currentIndex === 3">
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
          <dt>CV</dt>
          <dd>{{ cvFileName }}</dd>
        </div>
        <div class="recap__row">
          <dt>Lettre de motivation</dt>
          <dd>{{ lettreFileName ?? 'Non fournie' }}</dd>
        </div>
      </dl>
    </template>
  </CandidatureFlowShell>

  <CspDialog
    :open="succesOuvert"
    size="sm"
    title="Candidature envoyée"
    close-label="Fermer"
    @update:open="(value) => succesOuvert = value"
  >
    <div class="succes-popin">
      <span class="succes-popin__icon">
        <CspIcon
          name="ri:checkbox-circle-fill"
          :size="28"
        />
      </span>
      <p class="succes-popin__text">
        Votre candidature pour <strong>{{ offre.intitule }}</strong> a bien été envoyée.
        Vous recevrez une réponse par email dès qu'elle aura été étudiée.
      </p>
    </div>

    <template #footer>
      <CspButton
        variant="primary"
        label="Fermer"
        @click="succesOuvert = false"
      />
    </template>
  </CspDialog>
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

.piece {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.piece__label {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.piece__requis {
  font-weight: 400;
  color: var(--text-mention-grey);
}

.piece__optionnel {
  font-weight: 400;
  color: var(--text-mention-grey);
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

.succes-popin {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--csp-space-3);
}

.succes-popin__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background-color: var(--background-contrast-success);
  color: var(--text-default-success);
}

.succes-popin__text {
  margin: 0;
  color: var(--text-default-grey);
  line-height: 1.5;
}
</style>
