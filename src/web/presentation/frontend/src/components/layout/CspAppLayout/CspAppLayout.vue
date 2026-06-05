<script setup lang="ts"></script>

<template>
  <div class="csp-app-layout">
    <aside class="csp-app-layout__sidebar">
      <slot name="sidebar" />
    </aside>
    <main class="csp-app-layout__main">
      <slot />
    </main>
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
}

.csp-app-layout__main {
  flex: 1;
  min-width: 0;
  overflow-x: auto;
}
</style>
