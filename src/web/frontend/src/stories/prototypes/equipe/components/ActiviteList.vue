<script setup lang="ts">
import type { ProtoEvenement } from '../data/mock'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formatRelative } from '../shared/format'

defineProps<{
  evenements: ProtoEvenement[]
  emptyTitle: string
}>()
</script>

<template>
  <CspEmptyState
    v-if="evenements.length === 0"
    :title="emptyTitle"
    icon="ri:history-line"
  />
  <ol
    v-else
    class="activite-list"
  >
    <li
      v-for="evenement in evenements"
      :key="evenement.uuid"
      class="activite-list__item"
    >
      <span class="activite-list__icon">
        <CspIcon
          name="ri:user-settings-line"
          :size="16"
        />
      </span>
      <div class="activite-list__body">
        <p class="activite-list__libelle">
          <strong>{{ evenement.auteur }}</strong> {{ evenement.libelle }}
        </p>
        <p class="activite-list__date">
          {{ formatRelative(evenement.date) }}
        </p>
      </div>
    </li>
  </ol>
</template>

<style scoped lang="scss">
.activite-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.activite-list__item {
  display: flex;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) 0;
  border-bottom: 1px solid var(--border-default-grey);

  &:last-child {
    border-bottom: 0;
  }
}

.activite-list__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 0.25rem;
  background: var(--background-alt-grey);
  color: var(--text-mention-grey);
}

.activite-list__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.activite-list__libelle {
  margin: 0;
  font-size: var(--csp-font-size-base);
  line-height: var(--csp-line-height-base);
}

.activite-list__date {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
