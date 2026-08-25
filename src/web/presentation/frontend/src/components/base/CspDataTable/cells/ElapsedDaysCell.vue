<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import { formatElapsedDays } from '@/utils/date'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  {{ value ? formatElapsedDays(String(value)) : '-' }}
</template>
