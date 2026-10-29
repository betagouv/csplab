<script setup lang="ts">
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  count: number
}>()

const srLabel = computed(() => props.count
  ? `${props.count} ${pluralize(props.count, 'conversation')} non ${pluralize(props.count, 'lue')}`
  : 'Aucune conversation non lue')
</script>

<template>
  <span class="unread-conversations-indicator">
    <span class="sr-only">{{ srLabel }}</span>
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
