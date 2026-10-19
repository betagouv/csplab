<script setup lang="ts">
import CspCard from '@/components/base/CspCard/CspCard.vue'
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
      <CspCard
        v-for="card in cards"
        :key="card"
        as="div"
        size="sm"
        class="csp-skeleton-kanban__card"
      >
        <template #title>
          <CspSkeleton
            width="70%"
            variant="text"
          />
        </template>
        <div class="csp-skeleton-kanban__card-meta">
          <CspSkeleton
            width="45%"
            variant="text"
          />
        </div>
      </CspCard>
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-skeleton-kanban {
  display: flex;
  flex: 1;
  gap: var(--csp-kanban-gap);
  overflow: hidden;
  min-height: 0;
  padding-bottom: var(--csp-kanban-padding-bottom);
}

.csp-skeleton-kanban__column {
  display: flex;
  flex: 0 0 var(--csp-kanban-column-width);
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  min-width: var(--csp-kanban-column-width);
  padding: var(--csp-kanban-column-padding);
  background-color: var(--csp-region-background);
  box-shadow: inset 0 0 0 1px var(--csp-region-border-color);
  border-top: var(--csp-kanban-column-accent-width) solid var(--csp-category-accent-neutral);
}

.csp-skeleton-kanban__header {
  padding: 0 var(--csp-kanban-column-header-padding-inline);

  :deep(.csp-skeleton) {
    background: var(--csp-neutral-fill);
  }
}

.csp-skeleton-kanban__card.csp-card {
  --csp-card-bg: var(--csp-raised-background);
  --csp-card-border: var(--csp-raised-border);
}

.csp-skeleton-kanban__card-meta {
  margin-top: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}
</style>
