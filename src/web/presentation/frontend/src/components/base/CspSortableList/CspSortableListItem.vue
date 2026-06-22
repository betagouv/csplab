<script setup lang="ts" generic="T">
import { computed, ref } from 'vue'
import { SORTABLE_ITEM_TYPE, useDraggableElement } from '@/composables/dnd/useDraggableElement'
import { useDropTargetElement } from '@/composables/dnd/useDropTargetElement'

interface Props {
  item: T
  itemId: string
  index: number
  listId: string
  draggable?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  draggable: true,
  disabled: false,
})

const itemRef = ref<HTMLElement | null>(null)
const handleRef = ref<HTMLElement | null>(null)

const isInteractionEnabled = computed(() => !props.disabled)
const isDraggable = computed(() => props.draggable && isInteractionEnabled.value)
const position = computed(() => props.index + 1)

function getItemData() {
  return {
    type: SORTABLE_ITEM_TYPE,
    listId: props.listId,
    itemId: props.itemId,
    index: props.index,
  }
}

const { isDragging } = useDraggableElement({
  element: itemRef,
  dragHandle: handleRef,
  enabled: isDraggable,
  getInitialData: getItemData,
})

const { isDraggedOver, closestEdge } = useDropTargetElement({
  element: itemRef,
  enabled: isInteractionEnabled,
  canDrop: source => source.type === SORTABLE_ITEM_TYPE && source.listId === props.listId,
  getData: () => getItemData(),
})

function setHandleRef(element: Element | null) {
  handleRef.value = element as HTMLElement | null
}
</script>

<template>
  <li
    ref="itemRef"
    class="csp-sortable-list-item"
    :class="{
      'csp-sortable-list-item--dragging': isDragging,
      'csp-sortable-list-item--drag-over': isDraggedOver,
    }"
  >
    <div
      v-if="isDraggedOver && closestEdge === 'top'"
      class="csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top"
    />
    <slot
      :item="item"
      :index="props.index"
      :position="position"
      :is-dragging="isDragging"
      :is-dragged-over="isDraggedOver"
      :closest-edge="closestEdge"
      :set-handle-ref="setHandleRef"
      :is-draggable="isDraggable"
    />
    <div
      v-if="isDraggedOver && closestEdge === 'bottom'"
      class="csp-sortable-list-item__indicator csp-sortable-list-item__indicator--bottom"
    />
  </li>
</template>

<style scoped lang="scss">
.csp-sortable-list-item {
  position: relative;
  list-style: none;
}

.csp-sortable-list-item--dragging {
  opacity: 0.5;
}

.csp-sortable-list-item__indicator {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--background-action-high-blue-france);
  pointer-events: none;
}

.csp-sortable-list-item__indicator--top {
  top: calc(-1 * var(--csp-space-1));
}

.csp-sortable-list-item__indicator--bottom {
  bottom: calc(-1 * var(--csp-space-1));
}
</style>
