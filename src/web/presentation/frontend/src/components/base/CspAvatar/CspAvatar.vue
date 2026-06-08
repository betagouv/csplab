<script setup lang="ts">
import { computed } from 'vue'
import { getInitials } from '@/utils/format'

export interface CspAvatarProps {
  name?: string | null
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<CspAvatarProps>(), {
  size: 'md',
})

const initials = computed(() => {
  return getInitials(props.name)
})
</script>

<template>
  <div
    class="csp-avatar"
    :class="`csp-avatar--${size}`"
    role="img"
    :aria-label="name ?? undefined"
  >
    <span
      class="csp-avatar__initials"
      aria-hidden="true"
    >
      {{ initials ?? '?' }}
    </span>
  </div>
</template>

<style scoped lang="scss">
.csp-avatar {
  width: var(--csp-avatar-size);
  height: var(--csp-avatar-size);
  border-radius: 9999px;
  overflow: hidden;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  background-color: var(--background-contrast-grey);
  color: var(--text-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);

  font-weight: 700;
  font-size: var(--csp-avatar-font-size);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  user-select: none;
}

.csp-avatar__initials {
  line-height: 1;
}

.csp-avatar--sm {
  --csp-avatar-size: 1.5rem;
  --csp-avatar-font-size: 0.625rem;
}

.csp-avatar--md {
  --csp-avatar-size: 2rem;
  --csp-avatar-font-size: 0.75rem;
}

.csp-avatar--lg {
  --csp-avatar-size: 3rem;
  --csp-avatar-font-size: 1rem;
}
</style>
