<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  <template v-if="value">
    {{ value }}
  </template>
  <CspBadge
    v-else
    label="En attente"
    size="sm"
  />
</template>
