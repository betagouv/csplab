<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import UnreadConversationsIndicator from '../UnreadConversationsIndicator.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
}>()
</script>

<template>
  <UnreadConversationsIndicator :count="Number(value ?? 0)" />
</template>
