<script setup lang="ts">
import type { Offre } from '../store'
import { activiteOffre } from '../suivi'

// « Activité sur l'offre » : dernière activité significative, adaptée au statut (Alice, 25/11/2026).
defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
</script>

<template>
  <span class="activite">{{ activiteOffre(row) }}</span>
</template>

<style scoped lang="scss">
.activite {
  white-space: normal;
}
</style>
