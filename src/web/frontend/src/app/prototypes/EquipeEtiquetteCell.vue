<script setup lang="ts">
import type { Etiquette } from '@/features/candidatures/etiquettes'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: { etiquette?: Etiquette }
}>()
</script>

<template>
  <CspLabel
    v-if="row.etiquette"
    :label="row.etiquette.libelle"
    :color="row.etiquette.couleur"
  />
  <span v-else>-</span>
</template>
