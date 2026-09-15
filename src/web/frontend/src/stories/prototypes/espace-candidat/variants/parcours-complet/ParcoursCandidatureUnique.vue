<script setup lang="ts">
import { ref } from 'vue'
import CandidatureUnique from '../candidature-unique/CandidatureUnique.vue'
import PageOffre from '../offre/PageOffre.vue'

const etape = ref<'offre' | 'candidature'>('offre')

function surPostuler() {
  etape.value = 'candidature'
}
</script>

<template>
  <PageOffre
    v-if="etape === 'offre'"
    @postuler="surPostuler"
  />
  <CandidatureUnique v-else />
</template>
