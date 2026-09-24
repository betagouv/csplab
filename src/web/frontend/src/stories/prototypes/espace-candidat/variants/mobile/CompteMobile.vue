<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { useEspace } from '../../data/useEspace'
import MobileBottomSheet from '../../shared/mobile/MobileBottomSheet.vue'
import RetourLien from '../../shared/mobile/RetourLien.vue'

defineEmits<{
  retour: []
  deconnexion: []
}>()

const espace = useEspace()
const utilisateur = espace.utilisateur
const parFranceConnect = computed(() => utilisateur.methode === 'franceconnect')

const brouillon = reactive({
  prenom: utilisateur.prenom,
  nom: utilisateur.nom,
  telephone: utilisateur.telephone,
})
const enregistre = ref(false)

function enregistrer() {
  if (!parFranceConnect.value) {
    utilisateur.prenom = brouillon.prenom
    utilisateur.nom = brouillon.nom
  }
  utilisateur.telephone = brouillon.telephone
  enregistre.value = true
}

const motDePasseOuvert = ref(false)
const motDePasse = reactive({ actuel: '', nouveau: '', confirmation: '' })
const erreurMotDePasse = ref('')
const motDePasseModifie = ref(false)

function changerMotDePasse() {
  if (!motDePasse.actuel || motDePasse.nouveau.length < 8) {
    erreurMotDePasse.value = 'Saisissez votre mot de passe actuel et un nouveau mot de passe d\'au moins 8 caractères.'
    return
  }
  if (motDePasse.nouveau !== motDePasse.confirmation) {
    erreurMotDePasse.value = 'La confirmation ne correspond pas au nouveau mot de passe.'
    return
  }
  erreurMotDePasse.value = ''
  motDePasse.actuel = ''
  motDePasse.nouveau = ''
  motDePasse.confirmation = ''
  motDePasseOuvert.value = false
  motDePasseModifie.value = true
}
</script>

<template>
  <div class="compte">
    <RetourLien
      label="Mes candidatures"
      @retour="$emit('retour')"
    />

    <h1 class="compte__titre">
      Mon compte
    </h1>

    <CspCallout
      v-if="enregistre"
      variant="success"
      description="Vos modifications ont été enregistrées."
    />
    <CspCallout
      v-if="motDePasseModifie"
      variant="success"
      description="Votre mot de passe a été modifié."
    />

    <form
      class="compte__form"
      @submit.prevent="enregistrer"
    >
      <div class="compte__champ">
        <CspInput
          v-model="brouillon.prenom"
          label="Prénom"
          :disabled="parFranceConnect"
        />
      </div>
      <div class="compte__champ">
        <CspInput
          v-model="brouillon.nom"
          label="Nom"
          :disabled="parFranceConnect"
        />
        <p
          v-if="parFranceConnect"
          class="compte__aide"
        >
          Votre nom et votre prénom proviennent de FranceConnect et ne peuvent pas être modifiés ici.
        </p>
      </div>
      <div class="compte__champ">
        <CspInput
          :model-value="utilisateur.email"
          type="email"
          label="Adresse email"
          disabled
        />
        <p class="compte__aide">
          Votre adresse email ne peut pas être modifiée.
        </p>
      </div>
      <div class="compte__champ">
        <CspInput
          v-model="brouillon.telephone"
          type="tel"
          label="Téléphone"
        />
      </div>

      <CspButton
        type="submit"
        variant="primary"
        size="lg"
        label="Enregistrer"
        class="compte__bouton"
      />
    </form>

    <section
      v-if="!parFranceConnect"
      class="compte__section"
    >
      <h2>Mot de passe</h2>
      <CspButton
        variant="secondary"
        size="lg"
        icon="ri:lock-line"
        is-icon-left
        label="Modifier mon mot de passe"
        class="compte__bouton"
        @click="motDePasseOuvert = true"
      />
    </section>

    <CspButton
      variant="tertiary"
      size="lg"
      icon="ri:logout-box-line"
      is-icon-left
      label="Se déconnecter"
      class="compte__bouton compte__deconnexion"
      @click="$emit('deconnexion')"
    />

    <MobileBottomSheet
      v-model:open="motDePasseOuvert"
      title="Modifier mon mot de passe"
    >
      <CspCallout
        v-if="erreurMotDePasse"
        variant="error"
        :description="erreurMotDePasse"
      />
      <CspInput
        v-model="motDePasse.actuel"
        type="password"
        label="Mot de passe actuel"
      />
      <CspInput
        v-model="motDePasse.nouveau"
        type="password"
        label="Nouveau mot de passe"
      />
      <CspInput
        v-model="motDePasse.confirmation"
        type="password"
        label="Confirmer le nouveau mot de passe"
      />
      <template #footer>
        <CspButton
          variant="primary"
          size="lg"
          label="Enregistrer le mot de passe"
          class="compte__bouton"
          @click="changerMotDePasse"
        />
      </template>
    </MobileBottomSheet>
  </div>
</template>

<style scoped lang="scss">
.compte {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-2) var(--csp-space-4) var(--csp-space-8);
}

.compte__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.compte__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.compte__champ {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.compte__aide {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.compte__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-3);
  border-top: 1px solid var(--border-default-grey);

  h2 {
    margin: 0;
    font-size: 1.0625rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }
}

.compte__bouton {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}

.compte__deconnexion {
  margin-top: var(--csp-space-2);
}
</style>
