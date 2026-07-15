<script setup lang="ts">
import type { Candidature } from '../types'
import { ref, watchEffect } from 'vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useDraggableKanbanCard } from '@/composables/dnd/useKanbanDnd'
import { formatElapsedDays } from '@/utils/date'
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
    :title="formatCandidatNom(candidature.candidat)"
    class="candidature-kanban-card"
    :class="{ 'candidature-kanban-card--dragging': isDragging }"
  >
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

.candidature-kanban-card--dragging {
  opacity: 0.5;
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
