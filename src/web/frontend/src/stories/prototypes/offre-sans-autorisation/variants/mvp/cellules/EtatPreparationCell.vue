<script setup lang="ts">
import type { Offre } from '../store'
import { etatPreparation } from '../suivi'

// Onglet « En préparation » : un texte simple, sans badge (le badge répéterait le nom de l'onglet).
defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
</script>

<template>
  <span>{{ etatPreparation(row) }}</span>
</template>
