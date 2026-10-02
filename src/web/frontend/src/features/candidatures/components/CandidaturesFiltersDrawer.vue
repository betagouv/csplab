<script setup lang="ts">
import type { CspCheckboxGroupOption } from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'

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
  <CspFiltersDrawer
    v-model:open="open"
    :can-reset="canReset"
    @apply="emit('apply')"
    @reset="emit('reset')"
  >
    <CspCheckboxGroup
      v-model="etapes"
      label="Étapes de recrutement"
      :options="etapeOptions"
    />
  </CspFiltersDrawer>
</template>
