<script setup lang="ts">
import type { Candidature } from '../types'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formatElapsedDays } from '@/utils/date'
import { formatCandidatNom } from '../utils/candidat'

defineProps<{
  candidature: Candidature
}>()
</script>

<template>
  <article class="candidature-kanban-card">
    <h3 class="candidature-kanban-card__name">
      {{ formatCandidatNom(candidature.candidat) }}
    </h3>
    <p class="candidature-kanban-card__date">
      <CspIcon
        name="ri:calendar-line"
        class="candidature-kanban-card__date-icon"
        :size="14"
        aria-hidden="true"
      />
      {{ formatElapsedDays(candidature.date_soumission) }}
    </p>
  </article>
</template>

<style scoped lang="scss">
.candidature-kanban-card {
  padding: var(--csp-space-4);
  background-color: var(--background-default-grey);
  border-radius: 0.25rem;
  box-shadow: 0 1px 2px rgb(0 0 0 / 6%), inset 0 0 0 1px var(--border-default-grey);
}

.candidature-kanban-card__name {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text-title-grey);
  word-break: break-word;
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
