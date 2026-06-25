<script setup lang="ts">
import AtsAppShell from '../components/AtsAppShell.vue'
</script>

<template>
  <AtsAppShell>
    <div class="mes-recrutement-view">
      <h1 class="mes-recrutement-view__title">
        Mes recrutements
      </h1>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.mes-recrutement-view {
  padding: 2rem;
}

.mes-recrutement-view__title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
