<script setup lang="ts">
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'

const TITLE = 'Accueil'

useDocumentTitle(TITLE)
</script>

<template>
  <CspPageHeader
    :title="TITLE"
    subtitle="Bienvenue sur l'application de gestion des candidatures CSPLab."
  />
  <CspPageContainer />
</template>
