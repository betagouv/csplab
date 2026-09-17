<script setup lang="ts">
import type { Candidature } from '../types'
import { computed, ref, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useDraggableKanbanCard } from '@/composables/dnd/useKanbanDnd'
import { formatElapsedDays } from '@/utils/date'
import { CANDIDATURE_ROUTE_NAME } from '../routes'
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
  name: CANDIDATURE_ROUTE_NAME,
  params: { ...route.params, candidatureUuid: props.candidature.uuid },
}))

const isPanelOpen = computed(() => route.name === CANDIDATURE_ROUTE_NAME)

const { isDragging } = useDraggableKanbanCard({
  element: cardRef,
  boardId: props.boardId,
  columnId: props.columnId,
  cardId: props.candidature.uuid,
  cardIndex: props.cardIndex,
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
      'candidature-kanban-card--current': route.params.candidatureUuid === candidature.uuid,
    }"
    :data-candidature-uuid="candidature.uuid"
  >
    <template #title>
      <!-- draggable="false": the card starts the drag, not the link -->
      <RouterLink
        :to="panelLocation"
        :replace="isPanelOpen"
        draggable="false"
        class="candidature-kanban-card__link"
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
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-kanban-card {
  box-shadow:
    0 1px 2px rgb(0 0 0 / 6%),
    inset 0 0 0 1px var(--border-default-grey);
  cursor: grab;

  &:active {
    cursor: grabbing;
  }
}

.candidature-kanban-card:hover {
  --csp-card-bg: var(--background-alt-grey);
}

.candidature-kanban-card:focus-within {
  outline: 2px solid var(--csp-focus-ring-color);
  outline-offset: 2px;
}

.candidature-kanban-card--current {
  box-shadow:
    0 1px 2px rgb(0 0 0 / 6%),
    inset 0 0 0 2px var(--border-plain-info);
}

.candidature-kanban-card--dragging {
  opacity: 0.5;
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
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.candidature-kanban-card__date-icon {
  flex-shrink: 0;
}
</style>
