<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { EMPTY_CELL_TEXT, isEmptyCellValue } from '@/components/base/CspDataTable/table'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  <span v-if="isEmptyCellValue(value)">{{ EMPTY_CELL_TEXT }}</span>
  <CspBadge
    v-else
    :label="String(value)"
  />
</template>
