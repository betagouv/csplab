<script setup lang="ts">
defineProps<{
  email: string
}>()
</script>

<template>
  <div class="agent-email">
    <p class="agent-email__label">
      Courriel
    </p>
    <p class="agent-email__value">
      {{ email }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.agent-email {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-field-legend-gap);
}

.agent-email__label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: 600;
  color: var(--text-default-grey);
}

.agent-email__value {
  margin: 0;
  overflow-wrap: anywhere;
}
</style>
