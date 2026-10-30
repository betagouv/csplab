<script setup lang="ts">
import { useId } from 'vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  motif: string
}>()

const titleId = useId()
</script>

<template>
  <CspCard
    as="section"
    size="sm"
    class="candidature-motif-refus"
    :aria-labelledby="titleId"
  >
    <template #start>
      <h3
        :id="titleId"
        class="candidature-motif-refus__title"
      >
        <CspIcon name="ri:error-warning-line" />
        Motif de refus
      </h3>
    </template>
    <p class="candidature-motif-refus__motif">
      {{ motif }}
    </p>
  </CspCard>
</template>

<style scoped lang="scss">
.candidature-motif-refus {
  --csp-card-border: var(--border-plain-error);
  --csp-card-gap: var(--csp-space-2);
}

.candidature-motif-refus__title {
  display: flex;
  gap: var(--csp-space-1);
  align-items: center;
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-default-error);
}

.candidature-motif-refus__motif {
  margin: 0;
  color: var(--text-title-grey);
}
</style>
