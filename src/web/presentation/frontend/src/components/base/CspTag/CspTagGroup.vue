<script setup lang="ts" generic="T extends string | number">
import type { CspTagSize } from './tag'
import { ToggleGroupRoot } from 'reka-ui'
import { provideCspTagGroup } from './useCspTagGroup'

const props = withDefaults(defineProps<{
  type?: 'single' | 'multiple'
  size?: CspTagSize
  disabled?: boolean
  loop?: boolean
}>(), {
  type: 'multiple',
  disabled: false,
  loop: true,
})

const model = defineModel<T | T[]>()

provideCspTagGroup({
  size: props.size,
  disabled: props.disabled,
})
</script>

<template>
  <ToggleGroupRoot
    v-model="model"
    class="csp-tag-group"
    :type="type"
    :disabled="disabled"
    :loop="loop"
    :roving-focus="true"
  >
    <slot />
  </ToggleGroupRoot>
</template>

<style scoped lang="scss">
.csp-tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
</style>
