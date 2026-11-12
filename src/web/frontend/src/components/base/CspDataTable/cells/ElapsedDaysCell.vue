<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import { EMPTY_CELL_TEXT, isEmptyCellValue } from '@/components/base/CspDataTable/table'
import { formatElapsedDays } from '@/utils/date'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  <template v-if="isEmptyCellValue(value)">
    {{ EMPTY_CELL_TEXT }}
  </template>
  <template v-else>
    {{ formatElapsedDays(String(value)) }}
  </template>
</template>
