<script setup lang="ts">
import { reactive } from 'vue'
import FranceConnectButton from '../../shared/mobile/FranceConnectButton.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'

const identifiants = reactive({ email: '', motDePasse: '' })

defineEmits<{
  connecter: []
  franceConnect: []
  creerEspace: []
}>()
</script>

<template>
  <div class="connexion">
    <div class="connexion__content">
      <p class="connexion__eyebrow">
        Espace candidat
      </p>
      <h1 class="connexion__titre">
        Suivre mes candidatures
      </h1>
      <p class="connexion__sous-titre">
        La connexion n'est jamais nécessaire pour candidater — elle sert uniquement à retrouver
        vos candidatures et vos échanges au même endroit.
      </p>

      <FranceConnectButton @click="$emit('franceConnect')" />

      <div class="connexion__separateur">
        <CspSeparator />
        <span>ou</span>
        <CspSeparator />
      </div>

      <form
        class="connexion__form"
        @submit.prevent="$emit('connecter')"
      >
        <CspInput
          v-model="identifiants.email"
          type="email"
          label="Adresse email"
        />
        <CspInput
          v-model="identifiants.motDePasse"
          type="password"
          label="Mot de passe"
        />
        <button
          type="button"
          class="connexion__mdp-oublie"
        >
          Mot de passe oublié ?
        </button>
        <CspButton
          type="submit"
          variant="primary"
          size="lg"
          label="Se connecter"
          class="connexion__submit"
        />
      </form>

      <p class="connexion__creer">
        Pas encore d'espace candidat ?
        <button
          type="button"
          class="connexion__creer-lien"
          @click="$emit('creerEspace')"
        >
          Créer mon espace candidat
        </button>
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.connexion {
  min-height: 100vh;
  background-color: var(--background-default-grey);
  display: flex;
  justify-content: center;
}

.connexion__content {
  width: 100%;
  max-width: 26rem;
  padding: var(--csp-space-8) var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.connexion__eyebrow {
  margin: 0;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-action-high-blue-france);
}

.connexion__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.connexion__sous-titre {
  margin: 0 0 var(--csp-space-2);
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-mention-grey);
}

.connexion__separateur {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  margin: var(--csp-space-2) 0;
  color: var(--text-mention-grey);
  font-size: 0.8125rem;

  :deep(.csp-separator) {
    flex: 1;
    width: auto;
  }
}

.connexion__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.connexion__mdp-oublie {
  align-self: flex-start;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
}

.connexion__submit {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
  margin-top: var(--csp-space-2);
}

.connexion__creer {
  margin: var(--csp-space-4) 0 0;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.connexion__creer-lien {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  font: inherit;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
}
</style>
