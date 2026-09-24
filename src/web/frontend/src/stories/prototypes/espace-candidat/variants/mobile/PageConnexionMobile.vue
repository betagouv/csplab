<script setup lang="ts">
import { reactive, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import FranceConnectButton from '../../shared/mobile/FranceConnectButton.vue'

defineProps<{
  // Contexte d'arrivée (ex. lien « nouveau message » reçu par courriel).
  messageContexte?: string
  // Confirmation après une déconnexion.
  noticeDeconnexion?: string
}>()

const emit = defineEmits<{
  connecter: [methode: 'franceconnect' | 'formulaire']
}>()

const identifiants = reactive({ email: '', motDePasse: '' })
const erreur = ref('')
const vue = ref<'connexion' | 'oubli' | 'oubli-envoye'>('connexion')
const emailOubli = ref('')

function seConnecter() {
  if (!identifiants.email || !identifiants.motDePasse) {
    erreur.value = 'Renseignez votre adresse email et votre mot de passe.'
    return
  }
  erreur.value = ''
  emit('connecter', 'formulaire')
}

function envoyerLien() {
  vue.value = 'oubli-envoye'
}
</script>

<template>
  <div class="connexion">
    <div class="connexion__contenu">
      <div class="connexion__marque">
        <span class="connexion__logo">CSPLab</span>
        <span class="connexion__sous-logo">Espace candidat</span>
      </div>

      <template v-if="vue === 'connexion'">
        <h1 class="connexion__titre">
          Accéder à mon espace candidat
        </h1>
        <p class="connexion__texte">
          Suivez vos candidatures, répondez aux recruteurs et complétez votre dossier au même endroit.
        </p>

        <CspCallout
          v-if="messageContexte"
          variant="info"
          :description="messageContexte"
        />
        <CspCallout
          v-if="noticeDeconnexion"
          variant="success"
          :description="noticeDeconnexion"
        />

        <FranceConnectButton @click="emit('connecter', 'franceconnect')" />

        <div class="connexion__separateur">
          <CspSeparator />
          <span>ou</span>
          <CspSeparator />
        </div>

        <form
          class="connexion__form"
          @submit.prevent="seConnecter"
        >
          <p class="connexion__legende">
            Vous n'avez pas FranceConnect ? Connectez-vous avec votre adresse email.
          </p>
          <CspCallout
            v-if="erreur"
            variant="error"
            :description="erreur"
          />
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
            class="connexion__lien"
            @click="vue = 'oubli'"
          >
            Mot de passe oublié ?
          </button>
          <CspButton
            type="submit"
            variant="primary"
            size="lg"
            label="Se connecter"
            class="connexion__bouton"
          />
        </form>

        <p class="connexion__note">
          Pas besoin d'espace candidat pour postuler : il sert uniquement à suivre vos candidatures.
        </p>
      </template>

      <template v-else-if="vue === 'oubli'">
        <h1 class="connexion__titre">
          Mot de passe oublié
        </h1>
        <p class="connexion__texte">
          Saisissez l'adresse email de votre espace candidat : nous vous enverrons un lien pour
          choisir un nouveau mot de passe.
        </p>
        <form
          class="connexion__form"
          @submit.prevent="envoyerLien"
        >
          <CspInput
            v-model="emailOubli"
            type="email"
            label="Adresse email"
          />
          <CspButton
            type="submit"
            variant="primary"
            size="lg"
            label="Envoyer le lien de réinitialisation"
            class="connexion__bouton"
          />
        </form>
        <button
          type="button"
          class="connexion__lien"
          @click="vue = 'connexion'"
        >
          Retour à la connexion
        </button>
      </template>

      <template v-else>
        <h1 class="connexion__titre">
          Vérifiez votre boîte mail
        </h1>
        <CspCallout
          variant="success"
          description="Si un espace candidat existe pour cette adresse, un courriel contenant un lien de réinitialisation vient de lui être envoyé."
        />
        <CspButton
          variant="secondary"
          size="lg"
          label="Retour à la connexion"
          class="connexion__bouton"
          @click="vue = 'connexion'"
        />
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.connexion {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  background-color: var(--background-default-grey);
}

.connexion__contenu {
  width: 100%;
  max-width: 26rem;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) var(--csp-space-4) var(--csp-space-8);
}

.connexion__marque {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  margin-bottom: var(--csp-space-2);
}

.connexion__logo {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-action-high-blue-france);
}

.connexion__sous-logo {
  margin-top: 0.125rem;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.connexion__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.connexion__texte {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: var(--text-mention-grey);
}

.connexion__separateur {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
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

.connexion__legende {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-default-grey);
}

.connexion__lien {
  align-self: flex-start;
  min-height: 2.75rem;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
}

.connexion__bouton {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}

.connexion__note {
  margin: var(--csp-space-2) 0 0;
  text-align: center;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}
</style>
