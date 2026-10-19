<script setup lang="ts">
import type { Candidature } from '../types'
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import { useDraggableKanbanCard } from '@/composables/dnd/useKanbanDnd'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { formatElapsedDays } from '@/utils/date'
import { etiquettesOf } from '../etiquettes'
import { formatCandidatNom } from '../utils/candidat'

const props = defineProps<{
  candidature: Candidature
  boardId: string
  columnId: string
  cardIndex: number
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

const etiquettes = computed(() => etiquettesOf(props.candidature))

const { isDragging, isJustMoved, settleMove } = useDraggableKanbanCard({
  element: cardRef,
  boardId: props.boardId,
  columnId: props.columnId,
  cardId: props.candidature.uuid,
  cardIndex: props.cardIndex,
})

function handleAnimationEnd(event: AnimationEvent): void {
  if (event.target === event.currentTarget) {
    settleMove()
  }
}
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
    }"
    :aria-current="isCurrent ? 'true' : undefined"
    :data-csp-motion="isJustMoved ? 'color' : undefined"
    @animationend="handleAnimationEnd"
  >
    <template #title>
      <!-- draggable="false": the card starts the drag, not the link -->
      <RouterLink
        :to="panelLocation"
        draggable="false"
        class="candidature-kanban-card__link"
        :data-candidature-uuid="candidature.uuid"
      >
        {{ formatCandidatNom(candidature.candidat) }}
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
    <CspLabelList
      v-if="etiquettes.length"
      class="candidature-kanban-card__etiquettes"
      :labels="etiquettes"
      :max-lines="2"
    />
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-kanban-card {
  --candidature-kanban-card-raised-shadow: var(--csp-raised-shadow);
  --candidature-kanban-card-border: var(--csp-raised-border);
  --csp-card-bg: var(--csp-raised-background);

  box-shadow:
    var(--candidature-kanban-card-raised-shadow),
    inset 0 0 0 1px var(--candidature-kanban-card-border);
  cursor: grab;
  transition:
    background-color var(--csp-motion-duration-state),
    box-shadow var(--csp-motion-duration-state);

  &:active {
    cursor: grabbing;
  }
}

.candidature-kanban-card:hover {
  --csp-card-bg: var(--csp-raised-background-hover);
  --candidature-kanban-card-raised-shadow: var(--csp-raised-shadow-hover);
  --candidature-kanban-card-border: var(--csp-raised-border-hover);
}

/* inset: the scrolling column clips an outline drawn outside the card */
.candidature-kanban-card:has(.candidature-kanban-card__link:focus-visible) {
  outline: var(--csp-raised-focus-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-raised-focus-width));
  box-shadow:
    var(--candidature-kanban-card-raised-shadow),
    inset 0 0 0 calc(var(--csp-raised-focus-width) + 1px) var(--csp-raised-focus-gap-color);
}

.candidature-kanban-card--moved {
  animation: var(--csp-motion-raised-drop);
}

.candidature-kanban-card--current {
  --csp-card-bg: var(--csp-raised-current-background);

  box-shadow:
    var(--candidature-kanban-card-raised-shadow),
    inset 0 0 0 var(--csp-raised-current-border-width, 2px) var(--csp-raised-current-border-color),
    inset var(--csp-raised-current-bar-width, 0) 0 0 0 var(--csp-raised-current-bar-color, transparent);
}

.candidature-kanban-card--dragging {
  --candidature-kanban-card-raised-shadow: var(--csp-raised-shadow-drag);

  opacity: var(--csp-raised-drag-opacity);
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
  font-size: var(--csp-text-meta-size, var(--csp-font-size-sm));
  color: var(--text-mention-grey);
  font-weight: var(--csp-text-meta-weight, inherit);
  line-height: var(--csp-text-meta-line-height, inherit);
}

.candidature-kanban-card__date-icon {
  flex-shrink: 0;
}

.candidature-kanban-card__etiquettes {
  margin-top: var(--csp-space-2);
}

/* above the link overlay, so that « +N » takes the pointer */
.candidature-kanban-card__etiquettes :deep(.csp-label-list__more) {
  position: relative;
  z-index: 1;
}
</style>
