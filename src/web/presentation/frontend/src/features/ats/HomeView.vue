<script setup lang="ts">
import AtsAppShell from './components/AtsAppShell.vue'
</script>

<template>
  <AtsAppShell>
    <div class="home-view">
      <h1 class="home-view__title">
        Mes offres
      </h1>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.home-view {
  padding: var(--csp-space-8);
}

.home-view__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-2xl);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
