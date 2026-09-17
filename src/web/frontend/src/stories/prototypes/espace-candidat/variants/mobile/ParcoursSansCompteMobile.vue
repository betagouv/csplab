<script setup lang="ts">
import { ref } from 'vue'
import CandidatureSansCompteMobile from './CandidatureSansCompteMobile.vue'
import OffreMobile from './OffreMobile.vue'

const etape = ref<'offre' | 'candidature'>('offre')
</script>

<template>
  <OffreMobile
    v-if="etape === 'offre'"
    @postuler="etape = 'candidature'"
  />
  <CandidatureSansCompteMobile
    v-else
    @terminer="etape = 'offre'"
  />
</template>
