<script setup lang="ts">
import type { Offre } from '../store'
import ValidationBadge from '../ValidationBadge.vue'

defineOptions({ inheritAttrs: false })

defineProps<{ row: Offre }>()
</script>

<template>
  <ValidationBadge :offre="row" />
</template>
