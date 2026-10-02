<script setup lang="ts">
import type { Ref } from 'vue'
import type { TypeContrat } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { computed } from 'vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { FILTER_ALL, TYPE_CONTRAT_OPTIONS, withAllOption } from '../utils/filters'

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
const typeContrat = defineModel<TypeContrat | null>('typeContrat', { required: true })

function selectModel<T extends string>(model: Ref<T | null>) {
  return computed<string>({
    get: () => model.value ?? FILTER_ALL,
    set: (value) => {
      model.value = value === FILTER_ALL ? null : value as T
    },
  })
}

const responsableModel = selectModel(responsable)
const typeContratModel = selectModel(typeContrat)

const typeContratOptions = withAllOption('Tous les types', TYPE_CONTRAT_OPTIONS)
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
      v-model="typeContratModel"
      label="Type de contrat"
      :options="typeContratOptions"
    />
  </CspFiltersDrawer>
</template>
