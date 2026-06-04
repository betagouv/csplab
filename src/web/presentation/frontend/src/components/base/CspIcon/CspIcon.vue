<script setup lang="ts">
import { Icon as IconifyIcon } from '@iconify/vue'

interface CspIconProps {
  name: string
  size?: number | string
}

withDefaults(defineProps<CspIconProps>(), {
  size: 16,
})
</script>

<template>
  <IconifyIcon
    class="csp-icon"
    :icon="name"
    :width="size"
    :height="size"
    aria-hidden="true"
  />
</template>
