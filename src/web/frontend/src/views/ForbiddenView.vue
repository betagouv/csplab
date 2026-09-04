<script setup lang="ts">
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
</script>

<template>
  <CspPageHeader title="Accès refusé" />
  <CspPageContainer>
    <CspErrorState
      title="Vous n’avez pas accès à cette page."
      description="Votre compte n’est pas autorisé sur cet organisme. Rapprochez-vous de son responsable si vous pensez que c’est une erreur."
      icon="ri:lock-line"
    />
  </CspPageContainer>
</template>
