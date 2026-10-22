<script setup lang="ts">
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'

// Intitulé cliquable, en gras, comme dans la liste des recrutements de l'application.
defineOptions({ inheritAttrs: false })

defineProps<{
  value?: CspTableCellValue
  activate?: () => void
}>()
</script>

<template>
  <button
    type="button"
    class="titre-cell"
    @click="activate?.()"
  >
    {{ value }}
  </button>
</template>

<style scoped lang="scss">
.titre-cell {
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
