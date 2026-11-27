<script setup lang="ts">
import type { TagCategory } from '../types'
import type { CspSelectOption } from '@/components/base/CspSelect/CspSelect.vue'
import { computed } from 'vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { useCategoryTags } from '../composables/useCategoryTags'

const props = defineProps<{
  organismeUuid: string
  category: TagCategory
}>()

const model = defineModel<string | null>({ required: true })

const NO_TAG = 'none'

const { tags, pending, error } = useCategoryTags(props.organismeUuid, props.category)

const options = computed<CspSelectOption[]>(() => [
  { value: NO_TAG, label: 'Aucune étiquette' },
  ...tags.value.map(tag => ({ value: tag.uuid, label: tag.name })),
])

const unavailable = computed(() => !pending.value && !error.value && tags.value.length === 0)

const selected = computed({
  get: () => unavailable.value || error.value ? undefined : (model.value ?? NO_TAG),
  set: (value: string | undefined) => {
    model.value = !value || value === NO_TAG ? null : value
  },
})
</script>

<template>
  <CspSelect
    v-model="selected"
    label="Étiquette"
    :options="options"
    :placeholder="unavailable ? 'Aucune étiquette disponible.' : 'Aucune étiquette'"
    :disabled="pending || unavailable || Boolean(error)"
    :error="Boolean(error)"
    error-message="Les étiquettes n'ont pas pu être chargées."
  />
</template>
