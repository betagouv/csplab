<script setup lang="ts">
import { computed, useSlots } from 'vue'

const slots = useSlots()
const hasHeader = computed(() => Boolean(slots.header))
</script>

<template>
  <div class="csp-app-layout">
    <aside class="csp-app-layout__sidebar">
      <slot name="sidebar" />
    </aside>
    <div class="csp-app-layout__content">
      <header
        v-if="hasHeader"
        class="csp-app-layout__header"
      >
        <slot name="header" />
      </header>
      <main class="csp-app-layout__main">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--background-default-grey);
}

.csp-app-layout__sidebar {
  flex-shrink: 0;
  min-height: 100vh;
  overflow: hidden;
  background: var(--background-alt-grey);
  border-right: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: none;
  }
}

.csp-app-layout__content {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.csp-app-layout__header {
  display: none;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
  padding: 0.75rem 1rem;
  background: var(--background-default-grey);
  border-bottom: 1px solid var(--border-default-grey);

  @media (width <= 768px) {
    display: flex;
  }
}

.csp-app-layout__main {
  flex: 1;
  min-height: 0;
  overflow-x: auto;
}
</style>
