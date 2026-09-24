<script setup lang="ts">
import type { JeuDonnees, Utilisateur } from '../../data/espaceMock'
import type { CibleEspace } from './EspaceCandidatMobile.vue'
import { ref } from 'vue'
import EspaceCandidatMobile from './EspaceCandidatMobile.vue'
import PageConnexionMobile from './PageConnexionMobile.vue'

const props = withDefaults(defineProps<{
  jeu?: JeuDonnees
  simulerEchecEnvoi?: boolean
  // Écran visé par un lien de courriel : consommé à la première connexion.
  cible?: CibleEspace
  messageContexte?: string
}>(), {
  jeu: 'complet',
  simulerEchecEnvoi: false,
  cible: undefined,
  messageContexte: undefined,
})

const methode = ref<Utilisateur['methode'] | null>(null)
const cibleEnAttente = ref(props.cible)
const noticeDeconnexion = ref<string>()

function surConnexion(choisie: Utilisateur['methode']) {
  methode.value = choisie
  noticeDeconnexion.value = undefined
}

function surDeconnexion() {
  // Se déconnecter ferme aussi la session FranceConnect, le cas échéant.
  noticeDeconnexion.value = methode.value === 'franceconnect'
    ? 'Vous avez été déconnecté·e de votre espace candidat et de FranceConnect.'
    : 'Vous avez été déconnecté·e de votre espace candidat.'
  methode.value = null
  cibleEnAttente.value = undefined
}
</script>

<template>
  <PageConnexionMobile
    v-if="!methode"
    :message-contexte="cibleEnAttente ? messageContexte : undefined"
    :notice-deconnexion="noticeDeconnexion"
    @connecter="surConnexion"
  />
  <EspaceCandidatMobile
    v-else
    :jeu="jeu"
    :methode="methode"
    :simuler-echec-envoi="simulerEchecEnvoi"
    :cible="cibleEnAttente"
    @deconnexion="surDeconnexion"
  />
</template>
