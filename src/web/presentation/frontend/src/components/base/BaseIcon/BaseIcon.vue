<script setup lang="ts">
import { Icon as IconifyIcon } from '@iconify/vue'

interface BaseIconProps {
  /** Iconify name rendered by the component. */
  name: string
  /** Icon size in pixels or CSS units. */
  size?: number | string
}

withDefaults(defineProps<BaseIconProps>(), {
  size: 16,
})
</script>

<template>
  <IconifyIcon
    class="icon"
    :icon="name"
    :width="size"
    :height="size"
    aria-hidden="true"
  />
</template>
