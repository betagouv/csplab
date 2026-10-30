<script setup lang="ts">
import { useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  motif: string
}>()

const emit = defineEmits<{
  modifier: []
}>()

const titleId = useId()

const ACTIONS = [
  {
    items: [
      {
        label: 'Modifier le motif de refus',
        icon: 'ri:pencil-line',
        onSelect: () => emit('modifier'),
      },
    ],
  },
]
</script>

<template>
  <CspCard
    as="section"
    size="sm"
    class="candidature-motif-refus"
    :aria-labelledby="titleId"
  >
    <template #start>
      <div class="candidature-motif-refus__entete">
        <h3
          :id="titleId"
          class="candidature-motif-refus__title"
        >
          <CspIcon name="ri:error-warning-line" />
          Motif de refus
        </h3>
        <CspDropdownMenu
          :sections="ACTIONS"
          side="bottom"
          align="end"
        >
          <template #trigger>
            <CspButton
              icon="ri:more-fill"
              variant="tertiary-no-outline"
              size="sm"
              aria-label="Actions sur le motif de refus"
            />
          </template>
        </CspDropdownMenu>
      </div>
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

.candidature-motif-refus__entete {
  display: flex;
  flex: 1;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
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
