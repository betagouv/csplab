<script setup lang="ts">
import CspSkeleton from './CspSkeleton.vue'

export interface CspSkeletonSortableListProps {
  rows?: number
}

withDefaults(defineProps<CspSkeletonSortableListProps>(), {
  rows: 6,
})
</script>

<template>
  <div
    class="csp-skeleton-sortable-list"
    aria-hidden="true"
  >
    <div class="csp-skeleton-sortable-list__header">
      <CspSkeleton
        width="3rem"
        height="0.875rem"
      />
      <CspSkeleton
        width="10rem"
        height="0.875rem"
      />
      <CspSkeleton
        class="csp-skeleton-sortable-list__header-end"
        width="12rem"
        height="0.875rem"
      />
    </div>
    <div
      v-for="row in rows"
      :key="row"
      class="csp-skeleton-sortable-list__item"
    >
      <CspSkeleton
        width="1rem"
        height="1rem"
      />
      <CspSkeleton
        width="3rem"
        height="1rem"
      />
      <CspSkeleton
        width="30%"
        height="1.125rem"
      />
      <div class="csp-skeleton-sortable-list__item-end">
        <CspSkeleton
          width="7rem"
          height="1.5rem"
        />
        <CspSkeleton
          width="1.5rem"
          height="2rem"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-skeleton-sortable-list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.csp-skeleton-sortable-list__header {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-2) var(--csp-space-4);
}

.csp-skeleton-sortable-list__header-end {
  margin-left: auto;
}

.csp-skeleton-sortable-list__item {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  background-color: var(--background-default-grey);
}

.csp-skeleton-sortable-list__item-end {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  margin-left: auto;
}
</style>
