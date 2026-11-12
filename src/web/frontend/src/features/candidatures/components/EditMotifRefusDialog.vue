<script setup lang="ts">
import type { MotifRefus, MotifRefusOption } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import MotifRefusSelect from './MotifRefusSelect.vue'

const props = defineProps<{
  open: boolean
  currentMotif: MotifRefus
  motifs: MotifRefusOption[]
  motifsUnavailable?: boolean
  saving?: boolean
}>()

const emit = defineEmits<{
  confirm: [motifRefus: MotifRefus]
  cancel: []
}>()

const selection = ref<MotifRefus>()

watch(() => props.open, () => {
  selection.value = props.currentMotif
}, { immediate: true })

const newMotif = computed(() => props.motifs.find(motif => motif.value === selection.value && motif.value !== props.currentMotif))

function handleConfirm(): void {
  if (newMotif.value) {
    emit('confirm', newMotif.value.value)
  }
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Modifier le motif de refus"
    @update:open="(value) => { if (!value) { emit('cancel') } }"
  >
    <MotifRefusSelect
      v-model="selection"
      :motifs="motifs"
      :motifs-unavailable="motifsUnavailable"
    />

    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        @click="emit('cancel')"
      />
      <CspButton
        label="Enregistrer le motif"
        variant="primary"
        :disabled="!newMotif || saving"
        @click="handleConfirm"
      />
    </template>
  </CspDialog>
</template>
