<script setup lang="ts">
import type { ModeCandidature } from '../../shared/ChoixModeCandidature.vue'
import { ref } from 'vue'
import ChoixModeCandidature from '../../shared/ChoixModeCandidature.vue'
import CandidatureAvecCompte from '../candidature/CandidatureAvecCompte.vue'
import CandidatureAvecCv from '../candidature/CandidatureAvecCv.vue'
import CandidatureFormulaire from '../candidature/CandidatureFormulaire.vue'
import PageOffre from '../offre/PageOffre.vue'

type Etape = 'offre' | 'choix' | ModeCandidature

const etape = ref<Etape>('offre')

function surPostuler() {
  etape.value = 'choix'
}

function surChoix(mode: ModeCandidature) {
  etape.value = mode
}

function retourOffre() {
  etape.value = 'offre'
}
</script>

<template>
  <PageOffre
    v-if="etape === 'offre'"
    @postuler="surPostuler"
  />
  <ChoixModeCandidature
    v-else-if="etape === 'choix'"
    @choisir="surChoix"
    @retour="retourOffre"
  />
  <CandidatureAvecCv v-else-if="etape === 'cv'" />
  <CandidatureAvecCompte v-else-if="etape === 'compte'" />
  <CandidatureFormulaire v-else-if="etape === 'formulaire'" />
</template>
