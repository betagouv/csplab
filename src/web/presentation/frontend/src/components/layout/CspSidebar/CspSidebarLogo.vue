<script setup lang="ts">
import { useSidebar } from '@/composables/useSidebar'

const { isExpanded, isMobile } = useSidebar()
</script>

<template>
  <div class="csp-sidebar-logo">
    <span class="csp-sidebar-logo__title">CSPLab</span>
    <span
      v-if="isExpanded || isMobile"
      class="csp-sidebar-logo__subtitle"
    >
      ATS
    </span>
  </div>
</template>

<style scoped lang="scss">
.csp-sidebar-logo {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  min-width: 0;
}

.csp-sidebar-logo__title {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--text-action-high-blue-france);
  white-space: nowrap;
}

.csp-sidebar-logo__subtitle {
  margin-top: 0.125rem;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}
</style>
