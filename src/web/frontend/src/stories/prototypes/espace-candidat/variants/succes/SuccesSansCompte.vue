<script setup lang="ts">
import { offrePrincipale } from '../../data/candidatMock'
import CandidateHeader from '../../shared/CandidateHeader.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const offre = offrePrincipale
</script>

<template>
  <div class="succes">
    <CandidateHeader variant="public" />

    <main class="succes__main">
      <div class="succes__card">
        <span class="succes__icon">
          <CspIcon
            name="ri:checkbox-circle-fill"
            :size="32"
          />
        </span>

        <h1 class="succes__title">
          Candidature envoyée
        </h1>
        <p class="succes__subtitle">
          Pour l'offre <strong>{{ offre.intitule }}</strong> — {{ offre.organisme }}
        </p>

        <p class="succes__lead">
          Vous n'avez rien d'autre à faire pour le moment.
        </p>

        <div class="succes__section">
          <h2>Ce qui va se passer ensuite</h2>
          <p>Le recruteur va maintenant étudier votre candidature.</p>
        </div>

        <div class="succes__section">
          <h2>Comment vous serez informé·e</h2>
          <p>Vous recevrez un email si votre candidature évolue ou si le recruteur souhaite vous contacter.</p>
        </div>

        <div class="succes__note">
          <CspIcon
            name="ri:information-line"
            :size="18"
            class="succes__note-icon"
          />
          <div>
            <p class="succes__note-title">
              Vous n'avez pas besoin de créer un compte pour le moment.
            </p>
            <p class="succes__note-text">
              Si votre candidature avance, nous pourrons vous inviter à créer votre espace candidat
              pour suivre son évolution et échanger avec le recruteur.
            </p>
          </div>
        </div>

        <CspButton
          variant="tertiary"
          label="Retour aux offres"
          icon="ri:arrow-left-line"
          is-icon-left
          class="succes__back"
        />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.succes {
  min-height: 100vh;
  background-color: var(--background-alt-grey);
}

.succes__main {
  display: flex;
  justify-content: center;
  padding: var(--csp-space-8) var(--csp-space-6);
}

.succes__card {
  width: 100%;
  max-width: 32rem;
  background-color: var(--background-default-grey);
  border-radius: 0.5rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  padding: var(--csp-space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--csp-space-2);
}

.succes__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background-color: var(--background-contrast-success);
  color: var(--text-default-success);
  margin-bottom: var(--csp-space-2);
}

.succes__title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.succes__subtitle {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.succes__lead {
  margin: var(--csp-space-3) 0 var(--csp-space-2);
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.succes__section {
  width: 100%;
  text-align: left;
  padding-top: var(--csp-space-4);
  margin-top: var(--csp-space-2);
  border-top: 1px solid var(--border-default-grey);

  h2 {
    margin: 0 0 var(--csp-space-1);
    font-size: 0.9375rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }

  p {
    margin: 0;
    font-size: 0.875rem;
    color: var(--text-default-grey);
    line-height: 1.5;
  }
}

.succes__note {
  width: 100%;
  display: flex;
  gap: var(--csp-space-3);
  text-align: left;
  margin-top: var(--csp-space-4);
  padding: var(--csp-space-4);
  border-radius: 0.25rem;
  background-color: var(--background-alt-grey);
  color: var(--text-mention-grey);
}

.succes__note-icon {
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.succes__note-title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.succes__note-text {
  margin: 0.25rem 0 0;
  font-size: 0.8125rem;
  line-height: 1.5;
}

.succes__back {
  margin-top: var(--csp-space-6);
}
</style>
