<script setup lang="ts">
import type { UnreadVariant } from './variants'
import { provide, toRef } from 'vue'
import { UNREAD_VARIANT_KEY } from './variants'

const props = defineProps<{ variant: UnreadVariant }>()

provide(UNREAD_VARIANT_KEY, toRef(props, 'variant'))
</script>

<template>
  <slot />
</template>
