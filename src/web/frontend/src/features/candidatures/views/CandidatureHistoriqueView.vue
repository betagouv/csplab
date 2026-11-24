<script setup lang="ts">
import { computed } from 'vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { pluralize } from '@/utils/format'
import CandidatureActivitesList from '../components/CandidatureActivitesList.vue'
import { useCandidatureActivites } from '../composables/useCandidatureActivites'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}>()

const HISTORIQUE_SKELETON_COUNT = 5

const candidatureParams = computed(() => ({
  organismeUuid: props.organismeUuid,
  recrutementUuid: props.recrutementUuid,
  candidatureUuid: props.candidatureUuid,
}))
const { activites, total, pending, error } = useCandidatureActivites(() => candidatureParams.value)

const showSkeleton = useMinimumPending(pending)

const title = computed(() => `${total.value} ${pluralize(total.value, 'activité récente', 'activités récentes')}`)
</script>

<template>
  <section class="candidature-historique">
    <CspSkeleton
      v-if="showSkeleton"
      width="8rem"
      height="1.25rem"
      class="candidature-historique__skeleton"
    />
    <h3
      v-else-if="total > 0"
      class="candidature-historique__title"
    >
      {{ title }}
    </h3>
    <CandidatureActivitesList
      :activites="activites"
      :pending="showSkeleton"
      :error="error"
      :skeleton-count="HISTORIQUE_SKELETON_COUNT"
    />
  </section>
</template>

<style scoped lang="scss">
.candidature-historique__skeleton {
  margin-bottom: var(--csp-space-4);
}

.candidature-historique__title {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-mention-grey);
}
</style>
