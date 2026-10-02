<script setup lang="ts">
import type { CandidatureParams } from '../types'
import { computed, useId } from 'vue'
import { RouterLink } from 'vue-router'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useCandidatureActivites } from '../composables/useCandidatureActivites'
import { LATEST_ACTIVITES_LIMIT } from '../constants/candidature'
import { CANDIDATURE_PANEL_TAB_ROUTE_NAMES } from '../routes'
import CandidatureActivitesList from './CandidatureActivitesList.vue'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const { activites, pending, error } = useCandidatureActivites(() => props.candidature, LATEST_ACTIVITES_LIMIT)

const showSkeleton = useMinimumPending(pending)
const titleId = useId()

const historiqueLocation = computed(() => ({
  name: CANDIDATURE_PANEL_TAB_ROUTE_NAMES.historique,
  params: { ...props.candidature },
}))
</script>

<template>
  <section :aria-labelledby="titleId">
    <div class="candidature-activites__header">
      <h3
        :id="titleId"
        class="candidature-activites__title"
      >
        Dernières activités
      </h3>
      <RouterLink
        :to="historiqueLocation"
        class="candidature-activites__link"
      >
        Voir tout
      </RouterLink>
    </div>
    <CandidatureActivitesList
      :activites="activites"
      :pending="showSkeleton"
      :error="error"
      :skeleton-count="LATEST_ACTIVITES_LIMIT"
    />
  </section>
</template>

<style scoped lang="scss">
.candidature-activites__header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--csp-space-3);
  margin: 0 0 var(--csp-space-3);
}

.candidature-activites__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.candidature-activites__link {
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  text-underline-offset: 0.2em;

  &:hover {
    text-decoration-thickness: 2px;
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}
</style>
