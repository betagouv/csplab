<script setup lang="ts">
import AtsAppShell from './components/AtsAppShell.vue'
</script>

<template>
  <AtsAppShell>
    <div class="home-view">
      <h1 class="home-view__title">
        Mes offres
      </h1>
      <p class="home-view__hint">
        Layout de base branché. Le contenu métier viendra ensuite.
      </p>
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

.home-view__hint {
  margin: 0;
  color: var(--text-mention-grey);
}
</style>
