<script setup lang="ts">
import type { PartieOffre } from './etapes'
import type { Offre } from './store'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'

// Les champs d'une étape, les mêmes dans le formulaire de création et dans un bloc de la page de l'offre.
defineProps<{ offre: Offre, partie: PartieOffre, verrouilleCandidature?: boolean }>()
</script>

<template>
  <FormCandidature
    v-if="partie === 'formulaire' || partie === 'documents'"
    :offre="offre"
    :partie="partie"
    :verrouille="verrouilleCandidature"
  />
  <FormAnnonce
    v-else
    :offre="offre"
    :partie="partie"
  />
</template>
