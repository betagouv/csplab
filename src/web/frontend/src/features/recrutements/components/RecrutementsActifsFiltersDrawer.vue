<script setup lang="ts">
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { selectModel } from '../utils/filters'

defineProps<{
  responsableOptions: CspSelectOption[]
  canReset: boolean
}>()

const emit = defineEmits<{
  apply: []
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })
const responsable = defineModel<string | null>('responsable', { required: true })

const responsableModel = selectModel(responsable)
</script>

<template>
  <CspFiltersDrawer
    v-model:open="open"
    :can-reset="canReset"
    @apply="emit('apply')"
    @reset="emit('reset')"
  >
    <CspSelect
      v-model="responsableModel"
      label="Responsable"
      :options="responsableOptions"
    />
  </CspFiltersDrawer>
</template>
