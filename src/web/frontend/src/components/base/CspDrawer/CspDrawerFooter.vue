<script setup lang="ts">
import { useCspDrawerFooter } from './useCspDrawerFooter'

const footerId = useCspDrawerFooter()
</script>

<template>
  <Teleport
    defer
    :to="`#${footerId}`"
    :disabled="!footerId"
  >
    <slot />
  </Teleport>
</template>
