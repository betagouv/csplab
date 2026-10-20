<script setup lang="ts">
import { computed } from 'vue'
import { pluralize } from '@/utils/format'

const props = withDefaults(defineProps<{
  count?: string
  selectionCount?: number
  selectionLabel?: string
  bordered?: boolean
}>(), {
  count: undefined,
  selectionCount: 0,
  selectionLabel: undefined,
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
    <template v-if="selectionCount > 0">
      <p class="csp-table-toolbar__count">
        {{ selectionCountLabel }}
      </p>
      <div class="csp-table-toolbar__actions">
        <slot name="selection-actions" />
      </div>
    </template>
    <template v-else>
      <slot name="status">
        <p class="csp-table-toolbar__count">
          {{ count }}
        </p>
      </slot>
      <div class="csp-table-toolbar__actions">
        <slot />
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.csp-table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) 0;

  @include bp.from(bp.$md) {
    margin-inline: calc(-1 * var(--csp-table-toolbar-border-outset));
    padding-inline: var(--csp-table-toolbar-border-outset);
  }
}

.csp-table-toolbar--bordered {
  border-top: 1px solid var(--csp-table-toolbar-divider-color);
}

.csp-table-toolbar__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.csp-table-toolbar--selection .csp-table-toolbar__count {
  color: var(--text-default-grey);
  font-weight: 500;
}

.csp-table-toolbar__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}
</style>
