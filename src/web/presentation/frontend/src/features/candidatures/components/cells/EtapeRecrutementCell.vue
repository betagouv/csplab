<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  <CspBadge
    v-if="value"
    :label="value"
  />
  <span v-else>-</span>
</template>
