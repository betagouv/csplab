<script setup lang="ts">
export interface CspSkeletonProps {
  width?: string
  height?: string
  variant?: 'block' | 'text'
}

withDefaults(defineProps<CspSkeletonProps>(), {
  width: '100%',
  height: '1rem',
  variant: 'block',
})
</script>

<template>
  <span
    class="csp-skeleton"
    :class="{ 'csp-skeleton--text': variant === 'text' }"
    :style="{ width, height: variant === 'block' ? height : undefined }"
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

/* The box keeps the parent's line height; scaleY only thins the painted bar */
.csp-skeleton--text {
  height: 1lh;
  transform: scaleY(0.6);
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
