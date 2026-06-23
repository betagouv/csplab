<script setup lang="ts">
import AtsAppShell from './components/AtsAppShell.vue'
</script>

<template>
  <AtsAppShell>
    <div class="home-view">
      <h1 class="home-view__title">
        Accueil
      </h1>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.home-view {
  padding: 2rem;
}

.home-view__title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
