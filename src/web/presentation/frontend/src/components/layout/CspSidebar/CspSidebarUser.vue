<script setup lang="ts">
import type { ComputedRef } from 'vue'
import { inject } from 'vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'

interface CspSidebarUserProps {
  name: string
  role?: string
}

defineProps<CspSidebarUserProps>()

const isExpanded = inject<ComputedRef<boolean>>('sidebar-expanded')
</script>

<template>
  <div
    class="csp-sidebar-user"
    :class="{ 'csp-sidebar-user--expanded': isExpanded }"
    :title="isExpanded ? undefined : name"
  >
    <CspAvatar
      :name="name"
      size="md"
    />
    <div
      v-if="isExpanded"
      class="csp-sidebar-user__info"
    >
      <span class="csp-sidebar-user__name">{{ name }}</span>
      <span
        v-if="role"
        class="csp-sidebar-user__role"
      >{{ role }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-sidebar-user {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.625rem;
  width: 100%;
  min-width: 0;

  &--expanded {
    justify-content: flex-start;
    min-height: var(--sidebar-item-size, 2.5rem);
    padding: 0 var(--sidebar-inset-x, 0.5rem);
  }
}

.csp-sidebar-user__info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  line-height: 1.2;
}

.csp-sidebar-user__name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-user__role {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
