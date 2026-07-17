<script setup lang="ts">
withDefaults(defineProps<{
  fill?: boolean
}>(), {
  fill: false,
})
</script>

<template>
  <div
    class="csp-page-container"
    :class="{ 'csp-page-container--fill': fill }"
  >
    <slot />
  </div>
</template>

<style scoped lang="scss">
.csp-page-container {
  padding: var(--csp-space-8);
  box-sizing: border-box;
}

.csp-page-container--fill {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}
</style>
