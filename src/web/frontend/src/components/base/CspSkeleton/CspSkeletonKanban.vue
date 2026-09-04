<script setup lang="ts">
import CspSkeleton from './CspSkeleton.vue'

export interface CspSkeletonKanbanProps {
  columns?: number
  cards?: number
}

withDefaults(defineProps<CspSkeletonKanbanProps>(), {
  columns: 5,
  cards: 3,
})
</script>

<template>
  <div
    class="csp-skeleton-kanban"
    aria-hidden="true"
  >
    <div
      v-for="column in columns"
      :key="column"
      class="csp-skeleton-kanban__column"
    >
      <div class="csp-skeleton-kanban__header">
        <CspSkeleton
          width="60%"
          height="1.25rem"
        />
      </div>
      <div
        v-for="card in cards"
        :key="card"
        class="csp-skeleton-kanban__card"
      >
        <CspSkeleton
          width="70%"
          height="1.125rem"
        />
        <CspSkeleton
          width="45%"
          height="0.875rem"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-skeleton-kanban {
  display: flex;
  flex: 1;
  gap: var(--csp-space-3);
  overflow: hidden;
  min-height: 0;
}

.csp-skeleton-kanban__column {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  min-width: 18.75rem;
  padding: var(--csp-space-3);
  background-color: var(--background-alt-grey);
  border-top: 3px solid var(--border-default-grey);
}

.csp-skeleton-kanban__header {
  padding: 0 var(--csp-space-1);
}

.csp-skeleton-kanban__card {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  background: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}
</style>
