<script setup lang="ts">
import type { Candidat, MotifRefus, MotifRefusOption } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import { formatCandidatName } from '../format'
import MotifRefusSelect from './MotifRefusSelect.vue'

const props = defineProps<{
  open: boolean
  candidats: Candidat[]
  motifs: MotifRefusOption[]
  motifsUnavailable?: boolean
}>()

const emit = defineEmits<{
  confirm: [motifRefus: MotifRefus]
  cancel: []
}>()

const motifRefus = ref<MotifRefus>()

watch(() => props.open, () => {
  motifRefus.value = undefined
})

const description = computed(() => {
  const [candidat] = props.candidats
  if (props.candidats.length > 1 || !candidat) {
    return `Vous êtes sur le point de refuser ${props.candidats.length} candidatures. `
      + `Cette action n'est pas définitive, néanmoins les candidats seront informés du changement `
      + `de statut de leur candidature.`
  }
  return `Vous êtes sur le point de refuser la candidature de ${formatCandidatName(candidat)}. `
    + `Cette action n'est pas définitive, néanmoins le candidat sera informé du changement `
    + `de statut de sa candidature.`
})

function handleConfirm(): void {
  if (motifRefus.value) {
    emit('confirm', motifRefus.value)
  }
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Refus de candidature"
    @update:open="(value) => { if (!value) { emit('cancel') } }"
  >
    <div class="refus-candidature-dialog">
      <p class="refus-candidature-dialog__description">
        {{ description }}
      </p>

      <MotifRefusSelect
        v-model="motifRefus"
        hint="Champ obligatoire pour valider l'action"
        :motifs="motifs"
        :motifs-unavailable="motifsUnavailable"
      />
    </div>

    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        @click="emit('cancel')"
      />
      <CspButton
        label="Valider le refus"
        variant="primary"
        :disabled="!motifRefus"
        @click="handleConfirm"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.refus-candidature-dialog {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.refus-candidature-dialog__description {
  margin: 0;
}
</style>
