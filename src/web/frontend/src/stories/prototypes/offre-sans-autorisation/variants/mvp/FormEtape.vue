<script setup lang="ts">
import type { PartieOffre } from './etapes'
import type { Offre } from './store'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormDiffusion from './FormDiffusion.vue'

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
  <FormDiffusion
    v-else-if="partie === 'diffusion'"
    :offre="offre"
  />
  <FormAnnonce
    v-else
    :offre="offre"
    :partie="partie"
  />
</template>
