<script setup lang="ts">
import CspSkeleton from './CspSkeleton.vue'

export interface CspSkeletonTableProps {
  rows?: number
  columns?: number
  withHeader?: boolean
}

withDefaults(defineProps<CspSkeletonTableProps>(), {
  rows: 6,
  columns: 4,
  withHeader: true,
})
</script>

<template>
  <div
    class="csp-skeleton-table"
    :style="{ '--csp-skeleton-table-columns': columns }"
    aria-hidden="true"
  >
    <div
      v-if="withHeader"
      class="csp-skeleton-table__row csp-skeleton-table__row--header"
    >
      <CspSkeleton
        v-for="column in columns"
        :key="column"
        height="0.875rem"
        :width="column === 1 ? '60%' : '40%'"
      />
    </div>
    <div
      v-for="row in rows"
      :key="row"
      class="csp-skeleton-table__row"
    >
      <CspSkeleton
        v-for="column in columns"
        :key="column"
        height="1rem"
        :width="column === 1 ? '75%' : '55%'"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-skeleton-table {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
}

.csp-skeleton-table__row {
  display: grid;
  grid-template-columns: repeat(var(--csp-skeleton-table-columns), 1fr);
  align-items: center;
  gap: var(--csp-space-4);
  padding: 1rem 0.75rem;

  &:not(:last-child) {
    border-bottom: 1px solid var(--border-default-grey);
  }
}

.csp-skeleton-table__row--header {
  background: var(--background-alt-grey);

  :deep(.csp-skeleton) {
    background: var(--background-contrast-grey);
  }
}
</style>
