<script setup lang="ts">
import type { ActiviteEventName } from '../constants/candidature'
import type { Activite, CandidatureParams } from '../types'
import { useId } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { formatElapsedTime } from '@/utils/date'
import { useCandidatureActivites } from '../composables/useCandidatureActivites'
import { ACTIVITE_ICONS, ACTIVITE_LABELS, DEFAULT_ACTIVITE, LATEST_ACTIVITES_LIMIT } from '../constants/candidature'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const { activites, pending, error } = useCandidatureActivites(() => props.candidature)

const showSkeleton = useMinimumPending(pending)
const titleId = useId()

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
  <section :aria-labelledby="titleId">
    <h3
      :id="titleId"
      class="candidature-activites__title"
    >
      Dernières activités
    </h3>
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des activités"
      error-title="Les activités n'ont pas pu être chargées."
    >
      <template #skeleton>
        <div class="candidature-activites__list">
          <div
            v-for="index in LATEST_ACTIVITES_LIMIT"
            :key="index"
            class="candidature-activites__item"
          >
            <CspSkeleton
              width="1.75rem"
              height="1.75rem"
              class="candidature-activites__icon-skeleton"
            />
            <div class="candidature-activites__content">
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
        class="candidature-activites__list"
      >
        <li
          v-for="activite in activites"
          :key="`${activite.event_name}-${activite.occurred_at}`"
          class="candidature-activites__item"
        >
          <span class="candidature-activites__icon">
            <CspIcon
              :name="icon(activite)"
              :size="14"
              aria-hidden="true"
            />
          </span>
          <div class="candidature-activites__content">
            <p class="candidature-activites__label">
              {{ label(activite) }}
            </p>
            <p class="candidature-activites__meta">
              <span v-if="author(activite)">par {{ author(activite) }}</span>
              <time :datetime="activite.occurred_at">{{ formatElapsedTime(activite.occurred_at) }}</time>
            </p>
          </div>
        </li>
      </ol>
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.candidature-activites__title {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-activites__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.candidature-activites__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.candidature-activites__icon {
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

.candidature-activites__item .candidature-activites__icon-skeleton {
  flex-shrink: 0;
  border-radius: 50%;
}

.candidature-activites__content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
  padding-top: var(--csp-space-1);
}

.candidature-activites__label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  line-height: 1.4;
  color: var(--text-default-grey);
}

.candidature-activites__meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  line-height: 1.4;
  color: var(--text-mention-grey);
}
</style>
