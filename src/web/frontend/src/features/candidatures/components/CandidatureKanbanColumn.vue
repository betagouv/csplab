<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import { useDropTargetKanbanColumn } from '@/composables/dnd/useKanbanDnd'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import CandidatureKanbanCard from './CandidatureKanbanCard.vue'

const props = defineProps<{
  etape: EtapeRecrutementDetailedCandidatures
  boardId: string
  isSelected?: boolean
}>()

const emit = defineEmits<{
  toggleSelection: [etape: EtapeRecrutementDetailedCandidatures]
}>()

const categorieConfig = computed(() => CATEGORIE_CONFIG[props.etape.categorie])

const columnRef = ref<HTMLElement | null>(null)
const cardsRef = ref<HTMLElement | null>(null)

const { isDraggedOver } = useDropTargetKanbanColumn({
  element: columnRef,
  boardId: props.boardId,
  columnId: props.etape.uuid,
})

function scrollToEnd(): void {
  if (cardsRef.value) {
    cardsRef.value.scrollTop = cardsRef.value.scrollHeight
  }
}

defineExpose({ scrollToEnd })

function handleCheckboxChange(): void {
  emit('toggleSelection', props.etape)
}
</script>

<template>
  <section
    ref="columnRef"
    class="candidature-kanban-column"
    :class="[
      `candidature-kanban-column--${categorieConfig.cssModifier}`,
      { 'candidature-kanban-column--drag-over': isDraggedOver },
    ]"
  >
    <header class="candidature-kanban-column__header">
      <h2 class="candidature-kanban-column__title">
        <CspCheckbox
          :model-value="isSelected"
          class="candidature-kanban-column__select"
          variant="checkbox-only"
          size="sm"
          :label="`Sélectionner la colonne ${etape.nom}`"
          @update:model-value="handleCheckboxChange"
        />
        <span class="candidature-kanban-column__title-text">{{ etape.nom }}</span>
        <CspBadge
          class="candidature-kanban-column__count"
          size="md"
          variant="default"
          :label="String(etape.candidatures.length)"
        />
      </h2>
    </header>
    <ul
      ref="cardsRef"
      class="candidature-kanban-column__cards"
    >
      <li
        v-for="(candidature, index) in etape.candidatures"
        :key="candidature.uuid"
        class="candidature-kanban-column__card-item"
      >
        <CandidatureKanbanCard
          :candidature="candidature"
          :board-id="boardId"
          :column-id="etape.uuid"
          :card-index="index"
        />
      </li>
    </ul>
    <footer class="candidature-kanban-column__hint">
      <p class="candidature-kanban-column__hint-label">
        Statut visible par le candidat
      </p>
      <CspBadge
        class="candidature-kanban-column__hint-badge"
        size="sm"
        :icon="categorieConfig.icon"
        :type="categorieConfig.type"
        :label="categorieConfig.label"
      />
    </footer>
  </section>
</template>

<style scoped lang="scss">
.candidature-kanban-column {
  --candidature-kanban-column-accent: var(--csp-category-accent-neutral);
  --candidature-kanban-column-surface: var(--csp-category-surface-neutral, transparent);

  position: relative;
  display: flex;
  flex-direction: column;
  flex: 0 0 var(--csp-kanban-column-width);
  min-width: var(--csp-kanban-column-width);
  gap: var(--csp-kanban-column-gap);
  min-height: 12rem;
  max-height: 100%;
  padding: var(--csp-kanban-column-padding);
  background-color: var(--csp-region-background);
  box-shadow: inset 0 0 0 1px var(--csp-region-border-color);
  border-radius: var(--csp-radius-region);
  border-top: var(--csp-kanban-column-accent-width) solid var(--candidature-kanban-column-accent);

  /* Accent drawn inside the column, cut by its radius, when a theme sets --csp-kanban-column-accent-bar-width */
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(var(--candidature-kanban-column-accent), var(--candidature-kanban-column-accent)) top /
      100% var(--csp-kanban-column-accent-bar-width) no-repeat;
    pointer-events: none;
  }
}

.candidature-kanban-column--en-cours {
  --candidature-kanban-column-accent: var(--csp-category-accent-progress);
  --candidature-kanban-column-surface: var(--csp-category-surface-progress, transparent);
}

.candidature-kanban-column--refus {
  --candidature-kanban-column-accent: var(--csp-category-accent-negative);
  --candidature-kanban-column-surface: var(--csp-category-surface-negative, transparent);
}

.candidature-kanban-column--accepte {
  --candidature-kanban-column-accent: var(--csp-category-accent-positive);
  --candidature-kanban-column-surface: var(--csp-category-surface-positive, transparent);
}

.candidature-kanban-column--drag-over {
  background-color: var(--csp-region-drop-background);
  box-shadow: inset 0 0 0 var(--csp-region-drop-border-width) var(--csp-region-drop-border-color);
}

.candidature-kanban-column__header {
  margin: calc(-1 * var(--csp-kanban-column-padding)) calc(-1 * var(--csp-kanban-column-padding)) 0;
  padding: var(--csp-kanban-column-padding)
    calc(var(--csp-kanban-column-padding) + var(--csp-kanban-column-header-padding-inline))
    var(--csp-kanban-column-header-padding-bottom);
  background-color: var(--candidature-kanban-column-surface);
  border-bottom: var(--csp-kanban-column-header-divider-width) solid var(--csp-surface-divider-color);
}

.candidature-kanban-column__title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-text-group-title-size, 0.9375rem);
  font-weight: var(--csp-text-group-title-weight, 700);
  line-height: var(--csp-text-group-title-line-height, 1.3);
  color: var(--text-title-grey);
}

.candidature-kanban-column__title-text {
  min-width: 0;
}

.candidature-kanban-column__select {
  flex-shrink: 0;
}

.candidature-kanban-column__count {
  flex-shrink: 0;
  margin: 0;
}

.candidature-kanban-column__title :deep(.candidature-kanban-column__count.badge) {
  --badge-default-bg: var(--csp-region-badge-background);

  align-self: center;
}

.candidature-kanban-column__cards {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
  min-height: 0;

  @media (prefers-reduced-motion: no-preference) {
    scroll-behavior: smooth;
  }
}

.candidature-kanban-column__card-item {
  margin: 0;
}

.candidature-kanban-column__hint {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin-top: auto;
  padding: var(--csp-space-3) var(--csp-space-1) 0;
  border-top: 1px solid var(--csp-surface-divider-color);
}

.candidature-kanban-column__hint-label {
  margin: 0;
  font-size: var(--csp-text-caption-size, 0.75rem);
  color: var(--text-mention-grey);
  font-weight: var(--csp-text-caption-weight, inherit);
  line-height: var(--csp-text-caption-line-height, inherit);
}

.candidature-kanban-column__hint-badge {
  margin: 0;
}

.candidature-kanban-column__hint :deep(.candidature-kanban-column__hint-badge) {
  align-self: flex-start;
}

/* .badge outranks the background that CspBadge declares; the typed badges of the other categories keep theirs */
.candidature-kanban-column--entree
  .candidature-kanban-column__hint
  :deep(.candidature-kanban-column__hint-badge.badge) {
  --badge-default-bg: var(--csp-region-badge-background);
}
</style>
