<script setup lang="ts">
import type { MotifRefus, MotifRefusOption } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'

const props = defineProps<{
  open: boolean
  motifActuel: string
  motifs: MotifRefusOption[]
  motifsUnavailable?: boolean
  saving?: boolean
}>()

const emit = defineEmits<{
  confirm: [motifRefus: MotifRefus]
  cancel: []
}>()

const selection = ref<string>()

watch(() => props.open, () => {
  selection.value = props.motifActuel
}, { immediate: true })

const nouveauMotif = computed(() => props.motifs.find(motif => motif.value === selection.value && motif.value !== props.motifActuel))

function handleConfirm(): void {
  if (nouveauMotif.value) {
    emit('confirm', nouveauMotif.value.value)
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
    <CspSelect
      v-model="selection"
      label="Motif de refus"
      placeholder="Sélectionner un motif de refus"
      required
      :options="motifs"
      :error="motifsUnavailable"
      error-message="Les motifs de refus n'ont pas pu être chargés."
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
        :disabled="!nouveauMotif || saving"
        @click="handleConfirm"
      />
    </template>
  </CspDialog>
</template>
