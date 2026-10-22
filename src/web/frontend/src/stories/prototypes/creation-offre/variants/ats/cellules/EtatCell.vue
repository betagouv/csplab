<script setup lang="ts">
import type { Offre } from '../store'
import EtatBadge from '../EtatBadge.vue'

defineOptions({ inheritAttrs: false })

defineProps<{ row: Offre }>()
</script>

<template>
  <EtatBadge :etat="row.etat" />
</template>
