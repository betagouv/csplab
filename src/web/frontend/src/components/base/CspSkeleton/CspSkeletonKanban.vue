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
  border-radius: var(--csp-region-radius);
  border-top: var(--csp-category-accent-width) solid var(--csp-category-neutral-accent);
}

.csp-skeleton-kanban__card.csp-card {
  --csp-card-bg: var(--csp-raised-background);
  --csp-card-border: var(--csp-raised-border-color);

  box-shadow:
    var(--csp-raised-shadow, 0 0 transparent),
    inset 0 0 0 1px var(--csp-card-border);
}

.csp-skeleton-kanban__header {
  padding: 0 var(--csp-kanban-column-header-padding-inline) var(--csp-kanban-column-header-padding-bottom);
  border-bottom: var(--csp-kanban-column-header-divider-width) solid var(--csp-divider-color);

  :deep(.csp-skeleton) {
    background: var(--csp-neutral-background);
  }
}

.csp-skeleton-kanban__card-meta {
  margin-top: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}
</style>
