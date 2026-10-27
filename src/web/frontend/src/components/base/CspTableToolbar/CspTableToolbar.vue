<script setup lang="ts">
import { computed } from 'vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { pluralize } from '@/utils/format'

const props = withDefaults(defineProps<{
  count?: string
  pending?: boolean
  selectionCount?: number
  selectionLabel?: string
  selectionHint?: string
  bordered?: boolean
}>(), {
  count: undefined,
  pending: false,
  selectionCount: 0,
  selectionLabel: undefined,
  selectionHint: undefined,
  bordered: true,
})

const selectionCountLabel = computed(
  () => props.selectionLabel
    ?? `${props.selectionCount} ${pluralize(props.selectionCount, 'sélectionné')}`,
)
</script>

<template>
  <div
    class="csp-table-toolbar"
    :class="{
      'csp-table-toolbar--selection': selectionCount > 0,
      'csp-table-toolbar--bordered': bordered,
    }"
  >
    <div class="csp-table-toolbar__status">
      <slot name="start" />
      <template v-if="selectionCount > 0">
        <p class="csp-table-toolbar__count">
          {{ selectionCountLabel }}
        </p>
        <p
          v-if="selectionHint"
          class="csp-table-toolbar__hint"
        >
          {{ selectionHint }}
        </p>
      </template>
      <p
        v-else
        class="csp-table-toolbar__count"
      >
        <CspSkeleton
          v-if="pending"
          width="10rem"
          variant="text"
        />
        <template v-else>
          {{ count }}
        </template>
      </p>
    </div>
    <div class="csp-table-toolbar__actions">
      <slot
        v-if="selectionCount > 0"
        name="selection-actions"
      />
      <slot v-else />
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.csp-table-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) 0;
}

.csp-table-toolbar--bordered {
  border-top: 1px solid var(--border-default-grey);
}

.csp-table-toolbar__status {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2) var(--csp-space-4);
}

.csp-table-toolbar__count {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.5rem;
  color: var(--text-mention-grey);
}

.csp-table-toolbar--selection .csp-table-toolbar__count {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.csp-table-toolbar__hint {
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.25rem;
  color: var(--text-mention-grey);
}

.csp-table-toolbar__actions {
  display: flex;
  flex: 1 1 auto;
  flex-wrap: wrap;
  justify-content: flex-end;
  min-width: 0;
  align-items: center;
  gap: var(--csp-space-3);
}

.csp-table-toolbar__actions > :slotted(.csp-search-bar) {
  flex: 1 1 12rem;
  min-width: 0;

  @include bp.from(bp.$md) {
    flex: 0 1 auto;
    min-width: 20rem;
  }
}
</style>
