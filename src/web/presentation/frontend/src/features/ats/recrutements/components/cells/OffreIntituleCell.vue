<script setup lang="ts">
import type { RecrutementBase } from '../../types'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: RecrutementBase
  activate?: () => void
}>()
</script>

<template>
  <button
    type="button"
    class="intitule-cell"
    @click="activate?.()"
  >
    {{ row.intitule }}
  </button>
</template>

<style scoped lang="scss">
.intitule-cell {
  padding: 0;
  border: none;
  background: none;
  font: inherit;
  font-weight: 600;
  color: var(--text-title-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
