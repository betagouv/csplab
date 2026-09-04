<script setup lang="ts">
import type { CspCheckboxGroupOption } from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'

defineProps<{
  etapeOptions: CspCheckboxGroupOption[]
  canReset: boolean
}>()

const emit = defineEmits<{
  apply: []
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })
const etapes = defineModel<string[]>('etapes', { required: true })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Filtres"
    side="right"
    size="md"
  >
    <div class="filters-drawer">
      <CspCheckboxGroup
        v-model="etapes"
        label="Étapes de recrutement"
        :options="etapeOptions"
      />

      <div class="filters-drawer__actions">
        <CspButton
          label="Appliquer les filtres"
          variant="primary"
          @click="emit('apply')"
        />
        <CspButton
          label="Réinitialiser"
          variant="tertiary"
          icon="ri:refresh-line"
          is-icon-left
          :disabled="!canReset"
          @click="emit('reset')"
        />
      </div>
    </div>
  </CspDrawer>
</template>

<style scoped lang="scss">
.filters-drawer {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem 0;
}

.filters-drawer__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;

  &:deep(button) {
    /* @todo We should not do this but have a CspButtonGroup component instead */
    flex: 1;
  }
}
</style>
