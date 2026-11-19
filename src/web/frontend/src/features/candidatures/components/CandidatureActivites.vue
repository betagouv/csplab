<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import { computed, useId } from 'vue'
import { RouterLink } from 'vue-router'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useCandidatureActivites } from '../composables/useCandidatureActivites'
import { LATEST_ACTIVITES_LIMIT } from '../constants/candidature'
import CandidatureActivitesList from './CandidatureActivitesList.vue'
import CandidatureAsideTitle from './CandidatureAsideTitle.vue'

const props = defineProps<{
  candidature: CandidatureParams
  historiqueRouteName: string
}>()

const { activites, pending, error } = useCandidatureActivites(() => props.candidature, LATEST_ACTIVITES_LIMIT)

const showSkeleton = useMinimumPending(pending)
const titleId = useId()

const historiqueLocation = computed(() => ({
  name: props.historiqueRouteName,
  params: { ...props.candidature },
}))
</script>

<template>
  <section :aria-labelledby="titleId">
    <div class="candidature-activites__header">
      <CandidatureAsideTitle :id="titleId">
        Dernières activités
      </CandidatureAsideTitle>
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
