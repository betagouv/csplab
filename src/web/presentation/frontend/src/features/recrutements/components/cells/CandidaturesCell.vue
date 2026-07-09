<script setup lang="ts">
import type { RecrutementsActifs } from '../../types'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: RecrutementsActifs
}>()
</script>

<template>
  <div class="candidatures-cell">
    <span>{{ row.candidatures?.total ?? '-' }}</span>
    <span class="candidatures-cell__highlight">
      {{ row.candidatures?.a_traiter ?? '-' }}
    </span>
    <span>{{ row.candidatures?.en_cours ?? '-' }}</span>
  </div>
</template>

<style scoped lang="scss">
.candidatures-cell {
  display: inline-flex;
  align-items: center;
  gap: 1.25rem;
  font-variant-numeric: tabular-nums;
}

.candidatures-cell__highlight {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.75rem;
  padding: 0.125rem 0.375rem;
  background: var(--background-alt-grey);
  border-radius: 0.25rem;
  font-weight: 600;
}
</style>
