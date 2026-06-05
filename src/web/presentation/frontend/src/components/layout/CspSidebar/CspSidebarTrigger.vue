<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useSidebar } from '@/composables/useSidebar'

const { toggle, isMobile } = useSidebar()
</script>

<template>
  <CspButton
    v-if="isMobile"
    variant="tertiary-no-outline"
    size="sm"
    icon="ri:menu-line"
    aria-label="Ouvrir le menu"
    @click="toggle"
  />
</template>
