<script setup lang="ts" generic="T">
import { getReorderDestinationIndex } from '@atlaskit/pragmatic-drag-and-drop-hitbox/util/get-reorder-destination-index'
import { announce } from '@atlaskit/pragmatic-drag-and-drop-live-region'
import { monitorForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { reorder } from '@atlaskit/pragmatic-drag-and-drop/reorder'
import { onMounted, useId } from 'vue'
import { SORTABLE_ITEM_TYPE } from '@/composables/dnd/useDraggableElement'
import CspSortableListItem from './CspSortableListItem.vue'

interface Props {
  items: T[]
  getItemKey: (item: T) => string
  getItemLabel?: (item: T) => string
  isItemDraggable?: (item: T, index: number) => boolean
  getItemVariant?: (item: T, index: number) => 'default' | 'alt'
  disabled?: boolean
  showPosition?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  showPosition: false,
})

const emit = defineEmits<{
  reorder: [items: T[]]
}>()

const listId = useId()

function isDraggable(item: T, index: number) {
  if (props.disabled)
    return false
  return props.isItemDraggable?.(item, index) ?? true
}

function getVariant(item: T, index: number): 'default' | 'alt' {
  return props.getItemVariant?.(item, index) ?? 'default'
}

function getLabel(item: T): string {
  return props.getItemLabel?.(item) ?? props.getItemKey(item)
}

function isReorderValid(newItems: T[]): boolean {
  for (let i = 0; i < props.items.length; i++) {
    const original = props.items[i]
    if (isDraggable(original, i))
      continue
    if (props.getItemKey(newItems[i]) !== props.getItemKey(original))
      return false
  }
  return true
}

function tryReorder(fromIndex: number, toIndex: number) {
  if (props.disabled)
    return
  if (fromIndex === toIndex)
    return
  if (toIndex < 0 || toIndex >= props.items.length)
    return
  if (!isDraggable(props.items[fromIndex], fromIndex))
    return

  const newItems = reorder({ list: props.items, startIndex: fromIndex, finishIndex: toIndex })
  if (!isReorderValid(newItems))
    return

  emit('reorder', newItems)
  announce(`${getLabel(props.items[fromIndex])} déplacé`)
}

function canMoveUp(index: number): boolean {
  if (index <= 0)
    return false
  if (!isDraggable(props.items[index], index))
    return false
  return isDraggable(props.items[index - 1], index - 1)
}

function canMoveDown(index: number): boolean {
  if (index >= props.items.length - 1)
    return false
  if (!isDraggable(props.items[index], index))
    return false
  return isDraggable(props.items[index + 1], index + 1)
}

function createMoveUp(index: number) {
  return () => tryReorder(index, index - 1)
}

function createMoveDown(index: number) {
  return () => tryReorder(index, index + 1)
}

onMounted(() => {
  return monitorForElements({
    canMonitor: ({ source }) => source.data.type === SORTABLE_ITEM_TYPE && source.data.listId === listId,
    onDrop: ({ source, location }) => {
      if (props.disabled)
        return

      const destination = location.current.dropTargets[0]
      if (!destination)
        return

      const startIndex = source.data.index
      const indexOfTarget = destination.data.index

      if (typeof startIndex !== 'number' || typeof indexOfTarget !== 'number')
        return

      const closestEdgeOfTarget: 'top' | 'bottom' = indexOfTarget > startIndex ? 'bottom' : 'top'

      const finishIndex = getReorderDestinationIndex({
        startIndex,
        indexOfTarget,
        closestEdgeOfTarget,
        axis: 'vertical',
      })

      tryReorder(startIndex, finishIndex)
    },
  })
})
</script>

<template>
  <div class="csp-sortable-list">
    <div
      v-if="$slots.header"
      class="csp-sortable-list__header"
    >
      <span
        class="csp-sortable-list__header-handle-spacer"
        aria-hidden="true"
      />
      <div class="csp-sortable-list__header-content">
        <slot name="header" />
      </div>
    </div>
    <ul class="csp-sortable-list__items">
      <CspSortableListItem
        v-for="(item, index) in items"
        :key="getItemKey(item)"
        :item="item"
        :item-id="getItemKey(item)"
        :index="index"
        :list-id="listId"
        :draggable="isDraggable(item, index)"
        :variant="getVariant(item, index)"
        :disabled="disabled"
        :show-position="showPosition"
      >
        <template #default="slotProps">
          <slot
            name="item"
            v-bind="slotProps"
            :can-move-up="canMoveUp(index)"
            :can-move-down="canMoveDown(index)"
            :move-up="createMoveUp(index)"
            :move-down="createMoveDown(index)"
          />
        </template>
      </CspSortableListItem>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.csp-sortable-list__header {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}

.csp-sortable-list__header-handle-spacer {
  flex-shrink: 0;
  width: 1rem;
}

.csp-sortable-list__header-content {
  display: flex;
  flex: 1;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-2) var(--csp-space-4);
  font-size: var(--csp-font-size-sm);
  font-weight: 500;
  color: var(--text-mention-grey);
}

.csp-sortable-list__items {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
}
</style>
