<script setup lang="ts">
import type { CspTableSize } from '@/components/base/CspDataTable/table'
import CspSkeleton from './CspSkeleton.vue'

export interface CspSkeletonTableProps {
  rows?: number
  columns?: number
  withHeader?: boolean
  withFooter?: boolean
  size?: CspTableSize
}

withDefaults(defineProps<CspSkeletonTableProps>(), {
  rows: 6,
  columns: 4,
  withHeader: true,
  withFooter: false,
  size: 'md',
})
</script>

<template>
  <div
    class="csp-skeleton-table"
    :class="`csp-skeleton-table--${size}`"
    :style="{ '--csp-skeleton-table-columns': columns }"
    aria-hidden="true"
  >
    <div
      v-if="withHeader"
      class="csp-skeleton-table__head"
    >
      <div
        v-for="column in columns"
        :key="column"
        class="csp-skeleton-table__th"
      >
        <CspSkeleton
          variant="text"
          :width="column === 1 ? '60%' : '40%'"
        />
      </div>
    </div>
    <div
      v-for="row in rows"
      :key="row"
      class="csp-skeleton-table__row"
    >
      <div
        v-for="column in columns"
        :key="column"
        class="csp-skeleton-table__td"
      >
        <CspSkeleton
          variant="text"
          :width="column === 1 ? '75%' : '55%'"
        />
      </div>
    </div>
    <div
      v-if="withFooter"
      class="csp-skeleton-table__footer"
    >
      <CspSkeleton
        width="10rem"
        variant="text"
      />
      <CspSkeleton
        width="6rem"
        height="2rem"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;
@use '@/components/base/CspDataTable/table-sizes' as table;

.csp-skeleton-table {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
  border-radius: var(--csp-surface-radius, 0);
  background: var(--background-default-grey);
  overflow: hidden;
  font-size: var(--csp-font-size-base);

  @include table.sizes;
}

.csp-skeleton-table__head,
.csp-skeleton-table__row {
  display: grid;
  grid-template-columns: repeat(var(--csp-skeleton-table-columns), 1fr);
  border-bottom: 1px solid var(--csp-table-divider-color);
}

.csp-skeleton-table__head {
  background: var(--csp-table-head-background);
}

.csp-skeleton-table__footer {
  background: var(--csp-table-footer-background);
}

.csp-skeleton-table__head,
.csp-skeleton-table__footer {
  :deep(.csp-skeleton) {
    background: var(--csp-neutral-background);
  }
}

.csp-skeleton-table__row {
  min-height: var(--csp-table-row-height);

  &:last-child {
    border-bottom: none;
  }
}

.csp-skeleton-table__th,
.csp-skeleton-table__td {
  display: flex;
  align-items: center;
}

.csp-skeleton-table__th {
  padding: var(--csp-table-header-padding);
}

.csp-skeleton-table__td {
  padding: var(--csp-table-cell-padding);
}

.csp-skeleton-table__footer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-table-footer-padding);

  @include bp.from(bp.$md) {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
