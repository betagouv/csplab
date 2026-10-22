<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

// Étiquette courte (origine, catégorie…), même rendu que les étiquettes de candidature.
defineOptions({ inheritAttrs: false })

defineProps<{ value?: CspTableCellValue }>()
</script>

<template>
  <CspBadge
    v-if="value"
    :label="String(value)"
    size="sm"
  />
  <span v-else>-</span>
</template>
