<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { offrePrincipale } from '../data/candidatMock'
import CandidateHeader from './CandidateHeader.vue'

export type ModeCandidature = 'cv' | 'compte' | 'formulaire'

defineEmits<{
  choisir: [mode: ModeCandidature]
  retour: []
}>()

const offre = offrePrincipale

const options: { mode: ModeCandidature, icon: string, titre: string, description: string, duree: string }[] = [
  {
    mode: 'cv',
    icon: 'ri:file-upload-line',
    titre: 'Avec mon CV',
    description: 'Déposez votre CV : nous récupérons vos informations pour vous éviter de les ressaisir.',
    duree: 'Le plus rapide',
  },
  {
    mode: 'compte',
    icon: 'ri:user-add-line',
    titre: 'Avec un compte',
    description: 'Créez votre espace candidat pour suivre facilement toutes vos candidatures.',
    duree: 'Pour un suivi centralisé',
  },
  {
    mode: 'formulaire',
    icon: 'ri:file-list-3-line',
    titre: 'Avec un formulaire',
    description: 'Renseignez directement les informations demandées par l\'organisme.',
    duree: 'Sans dépôt de fichier',
  },
]
</script>

<template>
  <div class="choix">
    <CandidateHeader variant="public" />

    <main class="choix__main">
      <div class="choix__card">
        <button
          type="button"
          class="choix__retour"
          @click="$emit('retour')"
        >
          <CspIcon
            name="ri:arrow-left-line"
            :size="16"
          />
          Retour à l'offre
        </button>

        <h1 class="choix__title">
          Comment souhaitez-vous candidater ?
        </h1>
        <p class="choix__subtitle">
          Pour l'offre <strong>{{ offre.intitule }}</strong> — {{ offre.organisme }}.
          Choisissez la méthode qui vous convient le mieux, aucune n'exige de compte sauf
          la deuxième.
        </p>

        <div class="choix__options">
          <button
            v-for="option in options"
            :key="option.mode"
            type="button"
            class="choix__option"
            @click="$emit('choisir', option.mode)"
          >
            <span class="choix__option-icon">
              <CspIcon
                :name="option.icon"
                :size="22"
              />
            </span>
            <span class="choix__option-body">
              <span class="choix__option-titre">{{ option.titre }}</span>
              <span class="choix__option-description">{{ option.description }}</span>
              <span class="choix__option-duree">{{ option.duree }}</span>
            </span>
            <CspIcon
              name="ri:arrow-right-s-line"
              :size="20"
              class="choix__option-arrow"
            />
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.choix {
  min-height: 100vh;
  background-color: var(--background-alt-grey);
}

.choix__main {
  display: flex;
  justify-content: center;
  padding: var(--csp-space-8) var(--csp-space-6);
}

.choix__card {
  width: 100%;
  max-width: 36rem;
  background-color: var(--background-default-grey);
  border-radius: 0.5rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  padding: var(--csp-space-6);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.choix__retour {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  align-self: flex-start;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  margin-bottom: var(--csp-space-2);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);

  &:hover {
    color: var(--text-action-high-blue-france);
  }
}

.choix__title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.choix__subtitle {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  color: var(--text-mention-grey);
  line-height: 1.5;
}

.choix__options {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.choix__option {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--csp-space-4);
  width: 100%;
  text-align: left;
  padding: var(--csp-space-4);
  border: none;
  border-radius: 0.375rem;
  background-color: var(--background-alt-grey);
  cursor: pointer;
  font: inherit;

  &:hover {
    background-color: var(--background-alt-blue-france);

    .choix__option-arrow {
      color: var(--text-action-high-blue-france);
    }
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.choix__option-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background-color: var(--background-default-grey);
  color: var(--text-action-high-blue-france);
}

.choix__option-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.choix__option-titre {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.choix__option-description {
  margin-top: 0.125rem;
  font-size: 0.8125rem;
  color: var(--text-default-grey);
  line-height: 1.4;
}

.choix__option-duree {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
}

.choix__option-arrow {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
