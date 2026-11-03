<script setup lang="ts">
import type { Candidature } from '../types'
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useDraggableKanbanCard } from '@/composables/dnd/useKanbanDnd'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { formatElapsedDays } from '@/utils/date'
import { formatCandidatName } from '../format'

const props = defineProps<{
  candidature: Candidature
  boardId: string
  columnId: string
}>()

const cardComponentRef = ref<InstanceType<typeof CspCard> | null>(null)
const cardRef = ref<HTMLElement | null>(null)

watchEffect(() => {
  cardRef.value = (cardComponentRef.value?.$el as HTMLElement | undefined) ?? null
})

const route = useRoute()

const panelLocation = computed(() => ({
  name: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.tabs.candidature,
  params: { ...route.params, candidatureUuid: props.candidature.uuid },
}))

const isCurrent = computed(() => route.params.candidatureUuid === props.candidature.uuid)

const { isDragging, isJustMoved, isDropWaiting } = useDraggableKanbanCard({
  element: cardRef,
  boardId: props.boardId,
  columnId: props.columnId,
  cardId: props.candidature.uuid,
})
</script>

<template>
  <CspCard
    ref="cardComponentRef"
    as="article"
    size="sm"
    class="candidature-kanban-card"
    :class="{
      'candidature-kanban-card--dragging': isDragging,
      'candidature-kanban-card--current': isCurrent,
      'candidature-kanban-card--moved': isJustMoved,
      'candidature-kanban-card--drop-waiting': isDropWaiting,
    }"
    :aria-current="isCurrent ? 'true' : undefined"
  >
    <template #title>
      <!-- draggable="false": the card starts the drag, not the link -->
      <RouterLink
        :to="panelLocation"
        draggable="false"
        class="candidature-kanban-card__link"
        :data-candidature-uuid="candidature.uuid"
      >
        {{ formatCandidatName(candidature.candidat) }}
      </RouterLink>
    </template>
    <p class="candidature-kanban-card__date">
      <CspIcon
        name="ri:calendar-line"
        class="candidature-kanban-card__date-icon"
        :size="14"
        aria-hidden="true"
      />
      {{ formatElapsedDays(candidature.date_soumission) }}
    </p>
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-kanban-card {
  --candidature-kanban-card-shadow: var(--csp-raised-shadow);

  box-shadow:
    var(--candidature-kanban-card-shadow),
    inset 0 0 0 1px var(--border-default-grey);
  transition:
    background-color var(--csp-motion-duration-state),
    box-shadow var(--csp-motion-duration-state);
  cursor: grab;

  &:active {
    cursor: grabbing;
  }
}

.candidature-kanban-card:hover {
  --csp-card-bg: var(--csp-raised-background-hover);
  --candidature-kanban-card-shadow: var(--csp-raised-shadow-hover);
}

/* inset: the scrolling column clips an outline drawn outside the card */
.candidature-kanban-card:has(.candidature-kanban-card__link:focus-visible) {
  outline: 2px solid var(--csp-focus-ring-color);
  outline-offset: -2px;
}

.candidature-kanban-card--current {
  box-shadow:
    var(--candidature-kanban-card-shadow),
    inset 0 0 0 2px var(--border-plain-info);
}

/* above its neighbours while it plays the drop motion */
.candidature-kanban-card--moved {
  z-index: 1;
  animation: var(--csp-motion-raised-drop);
}

.candidature-kanban-card--drop-waiting {
  animation-play-state: paused;
}

/* the pointer stays over the card it picks up: the drag state wins over the hover state */
.candidature-kanban-card--dragging,
.candidature-kanban-card--dragging:hover {
  --candidature-kanban-card-shadow: var(--csp-raised-shadow-drag);

  opacity: var(--csp-raised-opacity-drag);
}

.candidature-kanban-card__link {
  color: inherit;
  text-decoration: none;
  background-image: none;
  outline: none;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
  }
}

.candidature-kanban-card__date {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.candidature-kanban-card__date-icon {
  flex-shrink: 0;
}
</style>
