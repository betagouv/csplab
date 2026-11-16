<script setup lang="ts">
import type { NatureOffre } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { NATURE_OFFRE_OPTIONS, selectModel, withAllOption } from '../utils/filters'

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
const natureOffre = defineModel<NatureOffre | null>('natureOffre', { required: true })

const responsableModel = selectModel(responsable)
const natureOffreModel = selectModel(natureOffre)

const natureOffreOptions = withAllOption('Toutes les natures', NATURE_OFFRE_OPTIONS)
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
    <CspSelect
      v-model="natureOffreModel"
      label="Nature du recrutement"
      :options="natureOffreOptions"
    />
  </CspFiltersDrawer>
</template>
