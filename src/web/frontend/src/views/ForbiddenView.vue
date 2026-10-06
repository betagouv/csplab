<script setup lang="ts">
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useDocumentTitle } from '@/composables/ui/useDocumentTitle'

const TITLE = 'Accès refusé'

useDocumentTitle(TITLE)
</script>

<template>
  <CspPageHeader :title="TITLE" />
  <CspPageContainer>
    <CspErrorState
      title="Vous n’avez pas accès à cette page."
      description="Votre compte n’est pas autorisé sur cet organisme. Rapprochez-vous de son superviseur si vous pensez que c’est une erreur."
      icon="ri:lock-line"
    />
  </CspPageContainer>
</template>
