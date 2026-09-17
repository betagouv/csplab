<script setup lang="ts">
import { ref } from 'vue'
import EspaceCandidatMobile from './EspaceCandidatMobile.vue'
import PageConnexionMobile from './PageConnexionMobile.vue'

const connecte = ref(false)
</script>

<template>
  <PageConnexionMobile
    v-if="!connecte"
    @connecter="connecte = true"
    @france-connect="connecte = true"
    @creer-espace="connecte = true"
  />
  <EspaceCandidatMobile v-else />
</template>
