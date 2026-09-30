<script setup lang="ts">
import type { CandidatureListe } from '../../types'
import { formatCandidatName } from '../../format'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: CandidatureListe
  activate?: () => void
}>()
</script>

<template>
  <button
    type="button"
    class="candidat-nom-cell"
    @click="activate?.()"
  >
    {{ formatCandidatName(row.candidat) }}
  </button>
</template>

<style scoped lang="scss">
.candidat-nom-cell {
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
