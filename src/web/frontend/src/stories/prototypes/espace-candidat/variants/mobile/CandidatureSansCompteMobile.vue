<script setup lang="ts">
import type { ReponsesQualification } from '../../shared/QuestionsQualification.vue'
import { computed, reactive, ref } from 'vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { offrePrincipale } from '../../data/candidatMock'
import MobileFileField from '../../shared/mobile/MobileFileField.vue'
import MobileFlowShell from '../../shared/mobile/MobileFlowShell.vue'
import QuestionsQualification from '../../shared/QuestionsQualification.vue'
import PopinSuccesMobile from './PopinSuccesMobile.vue'

defineEmits<{
  terminer: []
}>()

const offre = offrePrincipale
const steps = ['Mes coordonnées', 'CV et lettre', 'Questions', 'Récapitulatif']
const currentIndex = ref(0)
const succesOuvert = ref(false)

const coordonnees = reactive({ prenom: '', nom: '', email: '', telephone: '' })
const cvFileName = ref<string | null>(null)
const lettreFileName = ref<string | null>(null)
const reponses = ref<ReponsesQualification>({ titulaireFp: '', disponibleSeptembre: '', permisB: '' })

const isLastContentStep = computed(() => currentIndex.value === steps.length - 1)

const nextDisabled = computed(() => {
  if (currentIndex.value === 0) {
    return !coordonnees.prenom || !coordonnees.nom || !coordonnees.email
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
  if (currentIndex.value === 0) {
    return
  }
  currentIndex.value -= 1
}

function modifier(index: number) {
  currentIndex.value = index
}
</script>

<template>
  <MobileFlowShell
    :title="offre.intitule"
    :steps="steps"
    :current-index="currentIndex"
    :is-last-content-step="isLastContentStep"
    :next-disabled="nextDisabled"
    @back="back"
    @next="next"
  >
    <template v-if="currentIndex === 0">
      <div class="step-intro">
        <h1>Mes coordonnées</h1>
        <p>Pour recevoir des nouvelles de votre candidature. Aucune création de compte ici.</p>
      </div>
      <CspInput
        v-model="coordonnees.prenom"
        label="Prénom"
      />
      <CspInput
        v-model="coordonnees.nom"
        label="Nom"
      />
      <CspInput
        v-model="coordonnees.email"
        type="email"
        label="Adresse email"
      />
      <CspInput
        v-model="coordonnees.telephone"
        type="tel"
        label="Téléphone"
      />
    </template>

    <template v-else-if="currentIndex === 1">
      <div class="step-intro">
        <h1>CV et lettre de motivation</h1>
        <p>Vos fichiers seront transmis directement au recruteur.</p>
      </div>
      <MobileFileField
        label="CV"
        requis
        :file-name="cvFileName"
        @select="(name) => cvFileName = name"
        @remove="cvFileName = null"
      />
      <MobileFileField
        label="Lettre de motivation"
        :file-name="lettreFileName"
        @select="(name) => lettreFileName = name"
        @remove="lettreFileName = null"
      />
    </template>

    <template v-else-if="currentIndex === 2">
      <div class="step-intro">
        <h1>Quelques questions</h1>
        <p>{{ offre.organisme }} a ajouté 3 questions courtes pour cette offre.</p>
      </div>
      <QuestionsQualification
        v-model="reponses"
        :show-intro="false"
      />
    </template>

    <template v-else-if="currentIndex === 3">
      <div class="step-intro">
        <h1>Vérifiez votre candidature</h1>
        <p>Vous pouvez encore modifier chaque section avant l'envoi définitif.</p>
      </div>

      <div class="recap-section">
        <div class="recap-section__header">
          <h2>Mes coordonnées</h2>
          <button
            type="button"
            class="recap-section__modifier"
            @click="modifier(0)"
          >
            Modifier
          </button>
        </div>
        <p>{{ coordonnees.prenom }} {{ coordonnees.nom }}</p>
        <p>{{ coordonnees.email }} · {{ coordonnees.telephone || 'Non renseigné' }}</p>
      </div>

      <div class="recap-section">
        <div class="recap-section__header">
          <h2>Mon CV</h2>
          <button
            type="button"
            class="recap-section__modifier"
            @click="modifier(1)"
          >
            Modifier
          </button>
        </div>
        <p>{{ cvFileName }}</p>
      </div>

      <div class="recap-section">
        <div class="recap-section__header">
          <h2>Ma lettre de motivation</h2>
          <button
            type="button"
            class="recap-section__modifier"
            @click="modifier(1)"
          >
            Modifier
          </button>
        </div>
        <p>{{ lettreFileName ?? 'Non fournie' }}</p>
      </div>

      <div class="recap-section">
        <div class="recap-section__header">
          <h2>Mes réponses</h2>
          <button
            type="button"
            class="recap-section__modifier"
            @click="modifier(2)"
          >
            Modifier
          </button>
        </div>
        <p>Titulaire de la fonction publique : {{ reponses.titulaireFp || 'Non renseigné' }}</p>
        <p>Disponible à partir de septembre : {{ reponses.disponibleSeptembre || 'Non renseigné' }}</p>
        <p>Permis B : {{ reponses.permisB || 'Non renseigné' }}</p>
      </div>
    </template>
  </MobileFlowShell>

  <PopinSuccesMobile
    :open="succesOuvert"
    :offre="offre"
    @close="$emit('terminer')"
  />
</template>

<style scoped lang="scss">
.step-intro {
  h1 {
    margin: 0 0 var(--csp-space-1);
    font-size: 1.1875rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }

  p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-mention-grey);
    line-height: 1.5;
  }
}

.recap-section {
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  p {
    margin: 0.125rem 0 0;
    font-size: 0.875rem;
    color: var(--text-default-grey);
  }
}

.recap-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  h2 {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }
}

.recap-section__modifier {
  border: none;
  background: none;
  cursor: pointer;
  padding: var(--csp-space-1) var(--csp-space-2);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
}
</style>
