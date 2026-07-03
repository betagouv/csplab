<script setup lang="ts">
import type { Ref } from 'vue'
import type { KindContrat, TypeContrat } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { FILTER_ALL, KIND_CONTRAT_OPTIONS, TYPE_CONTRAT_OPTIONS, withAllOption } from '../filters'

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
const kindContrat = defineModel<KindContrat | null>('kindContrat', { required: true })

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
const kindContratModel = selectModel(kindContrat)

const typeContratOptions = withAllOption('Tous les types', TYPE_CONTRAT_OPTIONS)
const kindContratOptions = withAllOption('Toutes les natures', KIND_CONTRAT_OPTIONS)
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Filtres"
    side="right"
    size="md"
  >
    <div class="filters-drawer">
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
      <CspSelect
        v-model="kindContratModel"
        label="Nature du contrat"
        :options="kindContratOptions"
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
