<script setup lang="ts">
import type { ActiviteEventName } from '../constants/candidature'
import type { Activite } from '../types'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { formatElapsedTime } from '@/utils/date'
import { ACTIVITE_ICONS, ACTIVITE_LABELS, DEFAULT_ACTIVITE } from '../constants/candidature'

defineProps<{
  activites: Activite[]
  pending: boolean
  error: unknown
  skeletonCount: number
}>()

function isKnown(eventName: string): eventName is ActiviteEventName {
  return eventName in ACTIVITE_LABELS
}

function label(activite: Activite): string {
  return isKnown(activite.event_name) ? ACTIVITE_LABELS[activite.event_name] : DEFAULT_ACTIVITE.label
}

function icon(activite: Activite): string {
  return isKnown(activite.event_name) ? ACTIVITE_ICONS[activite.event_name] : DEFAULT_ACTIVITE.icon
}

function author(activite: Activite): string {
  return `${activite.utilisateur_prenom} ${activite.utilisateur_nom}`.trim()
}
</script>

<template>
  <CspAsyncSection
    :pending="pending"
    :error="error"
    loading-label="Chargement des activités"
    error-title="Les activités n'ont pas pu être chargées."
  >
    <template #skeleton>
      <div class="candidature-activites-list">
        <div
          v-for="index in skeletonCount"
          :key="index"
          class="candidature-activites-list__item"
        >
          <CspSkeleton
            width="1.75rem"
            height="1.75rem"
            class="candidature-activites-list__icon-skeleton"
          />
          <div class="candidature-activites-list__content">
            <CspSkeleton
              width="10rem"
              height="1.225rem"
            />
            <CspSkeleton
              width="7rem"
              height="1.05rem"
            />
          </div>
        </div>
      </div>
    </template>

    <CspEmptyState
      v-if="activites.length === 0"
      icon="ri:history-line"
      title="La candidature n'a aucune activité"
    />
    <ol
      v-else
      class="candidature-activites-list"
    >
      <li
        v-for="activite in activites"
        :key="`${activite.event_name}-${activite.occurred_at}`"
        class="candidature-activites-list__item"
      >
        <span class="candidature-activites-list__icon">
          <CspIcon
            :name="icon(activite)"
            :size="14"
            aria-hidden="true"
          />
        </span>
        <div class="candidature-activites-list__content">
          <p class="candidature-activites-list__label">
            {{ label(activite) }}
          </p>
          <p class="candidature-activites-list__meta">
            <span v-if="author(activite)">par {{ author(activite) }}</span>
            <time :datetime="activite.occurred_at">{{ formatElapsedTime(activite.occurred_at) }}</time>
          </p>
        </div>
      </li>
    </ol>
  </CspAsyncSection>
</template>

<style scoped lang="scss">
.candidature-activites-list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.candidature-activites-list__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.candidature-activites-list__icon {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  color: var(--text-action-high-grey);
  background-color: var(--background-alt-grey);
  border-radius: 50%;
}

.candidature-activites-list__item .candidature-activites-list__icon-skeleton {
  flex-shrink: 0;
  border-radius: 50%;
}

.candidature-activites-list__content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
  padding-top: var(--csp-space-1);
}

.candidature-activites-list__label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  line-height: 1.4;
  color: var(--text-default-grey);
}

.candidature-activites-list__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  line-height: 1.4;
  color: var(--text-mention-grey);
}
</style>
