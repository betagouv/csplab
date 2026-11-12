<script setup lang="ts">
import type { MotifRefus, MotifRefusOption } from '../types'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'

defineProps<{
  motifs: MotifRefusOption[]
  motifsUnavailable?: boolean
  hint?: string
}>()

const model = defineModel<MotifRefus>()
</script>

<template>
  <CspSelect
    v-model="model"
    label="Motif de refus"
    :hint="hint"
    placeholder="Sélectionner un motif de refus"
    required
    :options="motifs"
    :error="motifsUnavailable"
    error-message="Les motifs de refus n'ont pas pu être chargés."
  />
</template>
