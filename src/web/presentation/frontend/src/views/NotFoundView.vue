<script setup lang="ts">
import { RouterLink } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
</script>

<template>
  <CspPageHeader title="Page introuvable" />
  <CspPageContainer>
    <CspErrorState
      title="Cette page n’existe pas."
      description="Le lien est peut-être incorrect ou la page a été déplacée."
      icon="ri:compass-3-line"
    >
      <template #action>
        <CspButton
          :as="RouterLink"
          :to="{ name: 'home' }"
          label="Retour à l’accueil"
          variant="primary"
        />
      </template>
    </CspErrorState>
  </CspPageContainer>
</template>
