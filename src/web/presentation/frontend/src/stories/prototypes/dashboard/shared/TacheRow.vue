<script setup lang="ts">
import type { TacheDashboard } from '../data/dashboardMock'
import { computed } from 'vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = defineProps<{
  tache: TacheDashboard
}>()

const emit = defineEmits<{
  open: [id: string]
  toggleFait: [id: string]
}>()

const faitModel = computed({
  get: () => props.tache.fait,
  set: () => emit('toggleFait', props.tache.id),
})

const echeanceBadge = computed(() => {
  switch (props.tache.echeanceStatut) {
    case 'retard':
      return { type: 'error' as const }
    case 'aujourdhui':
      return { type: 'warning' as const }
    default:
      return { type: undefined }
  }
})

function open() {
  emit('open', props.tache.id)
}
</script>

<template>
  <li
    class="tache-row"
    :class="{ 'tache-row--fait': tache.fait }"
  >
    <CspCheckbox
      v-model="faitModel"
      variant="checkbox-only"
      :label="`Marquer « ${tache.libelle} » comme faite`"
      size="sm"
    />

    <button
      type="button"
      class="tache-row__main"
      @click="open"
    >
      <span class="tache-row__libelle">{{ tache.libelle }}</span>
      <span
        v-if="tache.recrutementIntitule"
        class="tache-row__contexte"
      >
        <CspIcon
          name="ri:briefcase-line"
          :size="12"
        />
        {{ tache.recrutementIntitule }}
      </span>
    </button>

    <CspBadge
      class="tache-row__echeance"
      :type="echeanceBadge.type"
      :label="tache.echeanceLabel"
    />

    <span class="tache-row__assigne">
      <CspAvatar
        :name="tache.assigneA"
        size="sm"
      />
      <span class="tache-row__assigne-label">{{ tache.assigneA }}</span>
    </span>
  </li>
</template>

<style scoped lang="scss">
.tache-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0;
  border-bottom: 1px solid var(--border-default-grey);

  &:last-child {
    border-bottom: none;
  }

  &--fait {
    .tache-row__libelle {
      color: var(--text-disabled-grey);
      text-decoration: line-through;
    }
  }
}

.tache-row__main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.125rem;
  flex: 1;
  min-width: 0;
  padding: 0.25rem;
  margin: -0.25rem;
  background: none;
  border: none;
  border-radius: 0.25rem;
  text-align: left;
  cursor: pointer;

  &:hover .tache-row__libelle {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.tache-row__libelle {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-title-grey);
}

.tache-row__contexte {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.tache-row__echeance {
  flex-shrink: 0;
}

.tache-row__assigne {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  flex-shrink: 0;
  min-width: 0;

  @media (width <= 640px) {
    display: none;
  }
}

.tache-row__assigne-label {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 6rem;
}
</style>
