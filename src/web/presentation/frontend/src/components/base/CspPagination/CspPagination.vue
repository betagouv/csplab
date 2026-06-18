<script setup lang="ts">
import {
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
  PaginationRoot,
} from 'reka-ui'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  pageCount: number
  siblingCount?: number
  showFirstLast?: boolean
  showDirectionLabels?: boolean
  disabled?: boolean
}>(), {
  siblingCount: 1,
  showFirstLast: true,
  showDirectionLabels: true,
  disabled: false,
})

const page = defineModel<number>('page', { required: true })
</script>

<template>
  <PaginationRoot
    v-model:page="page"
    class="csp-pagination"
    aria-label="Pagination"
    :total="pageCount"
    :items-per-page="1"
    :sibling-count="siblingCount"
    :disabled="disabled"
    show-edges
  >
    <PaginationList
      v-slot="{ items }"
      class="csp-pagination__list"
    >
      <PaginationFirst
        v-if="showFirstLast"
        class="csp-pagination__link csp-pagination__link--icon"
        aria-label="Première page"
        title="Première page"
        type="button"
      >
        <CspIcon
          name="ri:arrow-left-double-line"
          :size="16"
        />
      </PaginationFirst>

      <PaginationPrev
        class="csp-pagination__link csp-pagination__link--direction"
        aria-label="Page précédente"
        title="Page précédente"
        type="button"
      >
        <CspIcon
          name="ri:arrow-left-s-line"
          :size="16"
        />
        <span
          v-if="showDirectionLabels"
          class="csp-pagination__label csp-pagination__label--lg"
        >
          Précédente
        </span>
      </PaginationPrev>

      <template
        v-for="(item, index) in items"
        :key="index"
      >
        <PaginationListItem
          v-if="item.type === 'page'"
          class="csp-pagination__link"
          :title="`Page ${item.value}`"
          type="button"
          :value="item.value"
        >
          {{ item.value }}
        </PaginationListItem>
        <PaginationEllipsis
          v-else
          :index="index"
          class="csp-pagination__ellipsis"
        >
          …
        </PaginationEllipsis>
      </template>

      <PaginationNext
        class="csp-pagination__link csp-pagination__link--direction"
        aria-label="Page suivante"
        title="Page suivante"
        type="button"
      >
        <span
          v-if="showDirectionLabels"
          class="csp-pagination__label csp-pagination__label--lg"
        >
          Suivante
        </span>
        <CspIcon
          name="ri:arrow-right-s-line"
          :size="16"
        />
      </PaginationNext>

      <PaginationLast
        v-if="showFirstLast"
        class="csp-pagination__link csp-pagination__link--icon"
        aria-label="Dernière page"
        title="Dernière page"
        type="button"
      >
        <CspIcon
          name="ri:arrow-right-double-line"
          :size="16"
        />
      </PaginationLast>
    </PaginationList>
  </PaginationRoot>
</template>

<style scoped lang="scss">
.csp-pagination {
  display: flex;
  align-items: center;
  max-width: 100%;
  overflow-x: auto;
}

.csp-pagination__list {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  padding: 0;
  list-style: none;
  white-space: nowrap;
}

.csp-pagination__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  height: 2rem;
  padding: 0 var(--csp-space-1);
  border: none;
  background: none;
  font-size: var(--csp-font-size-sm);
  font-weight: 500;
  cursor: pointer;

  &:hover:not(:disabled) {
    background: var(--background-default-grey-hover);
  }

  &:active:not(:disabled) {
    background: var(--background-default-grey-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  &:disabled {
    color: var(--text-disabled-grey);
    cursor: not-allowed;
  }
}

.csp-pagination__link--icon {
  min-width: 2rem;
  padding: 0;
}

.csp-pagination__link--direction {
  gap: var(--csp-space-1);
}

.csp-pagination__link[data-selected] {
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-grey);
  cursor: default;

  &:hover:not(:disabled) {
    background: var(--background-action-high-blue-france-hover);
  }

  &:active:not(:disabled) {
    background: var(--background-action-high-blue-france-active);
  }
}

.csp-pagination__ellipsis {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.75rem;
  height: 2rem;
  color: var(--text-mention-grey);
}

.csp-pagination__label {
  display: none;
}

@media (width >= 62em) {
  .csp-pagination__label--lg {
    display: inline;
  }
}
</style>
