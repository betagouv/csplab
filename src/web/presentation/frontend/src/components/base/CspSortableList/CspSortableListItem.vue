<script setup lang="ts" generic="T">
import { computed, ref } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { SORTABLE_ITEM_TYPE, useDraggableElement } from '@/composables/dnd/useDraggableElement'
import { useDropTargetElement } from '@/composables/dnd/useDropTargetElement'

interface Props {
  item: T
  itemId: string
  index: number
  listId: string
  draggable?: boolean
  disabled?: boolean
  variant?: 'default' | 'alt'
}

const props = withDefaults(defineProps<Props>(), {
  draggable: true,
  disabled: false,
  variant: 'default',
})

const itemRef = ref<HTMLElement | null>(null)
const handleRef = ref<HTMLElement | null>(null)

const isInteractionEnabled = computed(() => !props.disabled)
const isDraggable = computed(() => props.draggable && isInteractionEnabled.value)

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
    :class="[
      `csp-sortable-list-item--${variant}`,
      {
        'csp-sortable-list-item--dragging': isDragging,
        'csp-sortable-list-item--drag-over': isDraggedOver,
      },
    ]"
  >
    <div
      v-if="isDraggedOver && closestEdge === 'top'"
      class="csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top"
    />

    <div class="csp-sortable-list-item__content">
      <span
        v-if="isDraggable"
        :ref="(el) => setHandleRef(el as Element | null)"
        class="csp-sortable-list-item__handle"
      >
        <CspIcon name="ri:draggable" :size="16" />
      </span>
      <span v-else class="csp-sortable-list-item__icon">
        <CspIcon name="ri:pushpin-2-line" :size="16" />
      </span>

      <slot
        :item="item"
        :index="props.index"
        :is-dragging="isDragging"
        :is-dragged-over="isDraggedOver"
        :closest-edge="closestEdge"
        :set-handle-ref="setHandleRef"
        :is-draggable="isDraggable"
      />
    </div>

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

.csp-sortable-list-item__content {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
  font-weight: 500;
}

.csp-sortable-list-item--alt .csp-sortable-list-item__content {
  background-color: var(--background-alt-grey);
}

.csp-sortable-list-item--dragging .csp-sortable-list-item__content {
  opacity: 0.5;
}

.csp-sortable-list-item__handle {
  display: flex;
  flex-shrink: 0;
  cursor: grab;
  color: var(--text-mention-grey);

  &:active {
    cursor: grabbing;
  }
}

.csp-sortable-list-item__icon {
  display: flex;
  flex-shrink: 0;
  color: var(--text-mention-grey);
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
