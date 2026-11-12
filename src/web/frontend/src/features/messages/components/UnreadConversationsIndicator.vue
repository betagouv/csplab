<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formatUnreadConversations } from '../format'

defineProps<{
  count: number
}>()
</script>

<template>
  <span class="unread-conversations-indicator">
    <span class="sr-only">{{ formatUnreadConversations(count) }}</span>
    <template v-if="count">
      <CspIcon
        name="ri:mail-unread-fill"
        :size="24"
        class="unread-conversations-indicator__icon"
      />
      <span aria-hidden="true">{{ count }}</span>
    </template>
    <span
      v-else
      aria-hidden="true"
    >-</span>
  </span>
</template>

<style scoped lang="scss">
.unread-conversations-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-variant-numeric: tabular-nums;
}

.unread-conversations-indicator__icon {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}
</style>
