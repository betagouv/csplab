<script setup lang="ts">
import type { ActionRequise } from '../data/candidatMock'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  action: ActionRequise
}>()

defineEmits<{
  agir: [action: ActionRequise]
}>()

const iconByType: Record<ActionRequise['type'], string> = {
  message: 'ri:message-3-line',
  document: 'ri:file-upload-line',
  entretien: 'ri:calendar-check-line',
}
</script>

<template>
  <div class="action-card">
    <span class="action-card__icon">
      <CspIcon
        :name="iconByType[action.type]"
        :size="18"
      />
    </span>
    <div class="action-card__body">
      <p class="action-card__tag">
        Action requise
      </p>
      <p class="action-card__label">
        {{ action.label }}
      </p>
    </div>
    <CspButton
      variant="secondary"
      size="sm"
      :label="action.cta"
      @click="$emit('agir', action)"
    />
  </div>
</template>

<style scoped lang="scss">
.action-card {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  background-color: var(--background-alt-yellow-tournesol);
  box-shadow: inset 0 0 0 1px var(--border-plain-yellow-tournesol);
}

.action-card__icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: var(--background-default-grey);
  color: var(--text-label-yellow-tournesol);
}

.action-card__body {
  flex: 1;
  min-width: 0;
}

.action-card__tag {
  margin: 0;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-label-yellow-tournesol);
}

.action-card__label {
  margin: 0.125rem 0 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
