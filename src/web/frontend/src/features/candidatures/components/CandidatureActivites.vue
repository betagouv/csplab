<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import { computed, useId } from 'vue'
import { RouterLink } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useCandidatureActivites } from '../composables/useCandidatureActivites'
import { LATEST_ACTIVITES_LIMIT } from '../constants/candidature'
import CandidatureActivitesList from './CandidatureActivitesList.vue'

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
      <h3
        :id="titleId"
        class="candidature-activites__title"
      >
        Dernières activités
      </h3>
      <CspButton
        :as="RouterLink"
        :to="historiqueLocation"
        variant="link"
        size="sm"
        label="Voir tout"
      />
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
</style>
