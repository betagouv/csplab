<script setup lang="ts">
import type { Candidature } from '../types'
import { computed, inject, ref, watchEffect } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { DEFAULT_UNREAD_VARIANT, UNREAD_VARIANT_KEY } from '@/app/prototypes/messages-non-lus/variants'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import { useDraggableKanbanCard } from '@/composables/dnd/useKanbanDnd'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { formatElapsedDays } from '@/utils/date'
import { etiquettesOf } from '../etiquettes'
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

const messagesLocation = computed(() => ({
  name: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.tabs.messages,
  params: { ...route.params, candidatureUuid: props.candidature.uuid },
}))

const unreadVariant = inject(UNREAD_VARIANT_KEY, ref(DEFAULT_UNREAD_VARIANT))
const unreadCount = computed(() => props.candidature.unread_conversations)
const unreadCountLabel = computed(() => unreadCount.value > 1
  ? `${unreadCount.value} conversations non lues`
  : '1 conversation non lue')

const isCurrent = computed(() => route.params.candidatureUuid === props.candidature.uuid)

const etiquettes = computed(() => etiquettesOf(props.candidature))

const { isDragging } = useDraggableKanbanCard({
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
    }"
    :aria-current="isCurrent ? 'true' : undefined"
  >
    <template
      v-if="unreadCount && unreadVariant === 'badge-statut'"
      #start
    >
      <CspBadge
        type="new"
        icon="ri:mail-unread-fill"
        label="Nouveau message"
      />
    </template>
    <template #title>
      <span class="candidature-kanban-card__title">
        <!-- draggable="false": the card starts the drag, not the link -->
        <RouterLink
          :to="panelLocation"
          draggable="false"
          class="candidature-kanban-card__link"
          :data-candidature-uuid="candidature.uuid"
        >
          {{ formatCandidatName(candidature.candidat) }}
        </RouterLink>
        <span
          v-if="unreadCount && unreadVariant === 'point-nom'"
          class="candidature-kanban-card__unread-dot"
          role="img"
          aria-label="Nouveau message"
        />
        <span
          v-if="unreadCount && unreadVariant === 'compteur-nom'"
          class="candidature-kanban-card__unread-count"
          role="img"
          :aria-label="unreadCountLabel"
        >{{ unreadCount }}</span>
      </span>
    </template>
    <p class="candidature-kanban-card__date">
      <CspIcon
        name="ri:calendar-line"
        class="candidature-kanban-card__date-icon"
        :size="14"
        aria-hidden="true"
      />
      {{ formatElapsedDays(candidature.date_soumission) }}
      <span
        v-if="unreadCount && unreadVariant === 'icone-date'"
        class="candidature-kanban-card__unread-meta"
      >
        <CspIcon
          name="ri:mail-unread-fill"
          class="candidature-kanban-card__unread-icon"
          :size="16"
          aria-hidden="true"
        />
        Nouveau message
      </span>
    </p>
    <p
      v-if="unreadCount && unreadVariant === 'maquette'"
      class="candidature-kanban-card__unread-line"
    >
      <span
        class="candidature-kanban-card__unread-line-dot"
        aria-hidden="true"
      />
      Nouveau message
    </p>
    <CspLabelList
      v-if="etiquettes.length"
      class="candidature-kanban-card__etiquettes"
      :labels="etiquettes"
      :max-lines="2"
    />
    <template
      v-if="unreadCount && unreadVariant === 'pied-lien'"
      #footer
    >
      <RouterLink
        :to="messagesLocation"
        draggable="false"
        class="candidature-kanban-card__unread-link"
      >
        <CspIcon
          name="ri:mail-unread-fill"
          :size="16"
          aria-hidden="true"
        />
        {{ unreadCount > 1 ? unreadCountLabel : 'Nouveau message' }}
        <CspIcon
          name="ri:arrow-right-line"
          class="candidature-kanban-card__unread-arrow"
          :size="16"
          aria-hidden="true"
        />
      </RouterLink>
    </template>
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-kanban-card {
  --candidature-kanban-card-shadow-rest: var(--csp-raised-shadow, 0 1px 2px rgba(0, 0, 0, 0.06));
  --candidature-kanban-card-shadow: var(--candidature-kanban-card-shadow-rest);
  --candidature-kanban-card-border: var(--csp-raised-border-color);
  --csp-card-bg: var(--csp-raised-background);

  box-shadow:
    var(--candidature-kanban-card-shadow),
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
  --csp-card-bg: var(--csp-raised-background-hover, var(--background-alt-grey));
  --candidature-kanban-card-shadow: var(--csp-raised-shadow-hover, var(--candidature-kanban-card-shadow-rest));
  --candidature-kanban-card-border: var(--csp-raised-border-color-hover, var(--csp-raised-border-color));
}

/* inset: the scrolling column clips an outline drawn outside the card */
.candidature-kanban-card:has(.candidature-kanban-card__link:focus-visible) {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: calc(-1 * var(--csp-focus-ring-width));
}

.candidature-kanban-card--current {
  --csp-card-bg: var(--csp-raised-background-current);

  box-shadow:
    var(--candidature-kanban-card-shadow),
    inset 0 0 0 var(--csp-raised-border-width-current) var(--csp-raised-border-color-current);
}

.candidature-kanban-card--dragging {
  --candidature-kanban-card-shadow: var(--csp-raised-shadow-drag, var(--candidature-kanban-card-shadow-rest));

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
  font-size: var(--csp-text-meta-size, var(--csp-font-size-sm));
  line-height: var(--csp-text-meta-line-height, inherit);
  font-weight: var(--csp-text-meta-weight, inherit);
  color: var(--text-mention-grey);
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
.candidature-kanban-card__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-2);
}

.candidature-kanban-card__unread-dot {
  flex-shrink: 0;
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
}

.candidature-kanban-card__unread-count {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 var(--csp-space-1);
  border-radius: 0.625rem;
  background-color: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1;
}

.candidature-kanban-card__unread-meta {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin-inline-start: auto;
  color: var(--text-default-grey);
  font-weight: var(--csp-font-weight-medium);
}

.candidature-kanban-card__unread-icon {
  color: var(--text-action-high-blue-france);
}

.candidature-kanban-card__unread-line {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-1) 0 0;
  color: var(--text-action-high-blue-france);
  font-size: var(--csp-text-meta-size, var(--csp-font-size-sm));
  line-height: var(--csp-text-meta-line-height, inherit);
}

.candidature-kanban-card__unread-line-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
}

/* above the link overlay, so that the link to the messages takes the pointer */
.candidature-kanban-card__unread-link {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  width: 100%;
  padding-top: var(--csp-space-2);
  box-shadow: inset 0 1px 0 var(--border-default-grey);
  color: var(--text-action-high-blue-france);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  background-image: none;

  &:hover {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.candidature-kanban-card__unread-arrow {
  margin-inline-start: auto;
}
</style>
