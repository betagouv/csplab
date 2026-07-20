<script setup lang="ts">
export interface CspSkeletonProps {
  width?: string
  height?: string
}

withDefaults(defineProps<CspSkeletonProps>(), {
  width: '100%',
  height: '1rem',
})
</script>

<template>
  <span
    class="csp-skeleton"
    :style="{ width, height }"
    aria-hidden="true"
  />
</template>

<style scoped lang="scss">
.csp-skeleton {
  display: block;
  max-width: 100%;
  border-radius: 0.25rem;
  background: var(--background-alt-grey);
  animation: csp-skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes csp-skeleton-pulse {
  50% {
    opacity: 0.5;
  }
}

@media (prefers-reduced-motion: reduce) {
  .csp-skeleton {
    animation: none;
  }
}
</style>
