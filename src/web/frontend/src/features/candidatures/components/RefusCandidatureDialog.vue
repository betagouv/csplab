<script setup lang="ts">
import type { Candidat, MotifRefus, MotifRefusOption } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { formatCandidatNom } from '../utils/candidat'

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
  return `Vous êtes sur le point de refuser la candidature de ${formatCandidatNom(candidat)}. `
    + `Cette action n'est pas définitive, néanmoins le candidat sera informé du changement `
    + `de statut de sa candidature.`
})

function handleConfirm(): void {
  if (motifRefus.value)
    emit('confirm', motifRefus.value)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Refus de candidature"
    @update:open="(value) => { if (!value) emit('cancel') }"
  >
    <div class="refus-candidature-dialog">
      <p class="refus-candidature-dialog__description">
        {{ description }}
      </p>

      <CspSelect
        v-model="motifRefus"
        label="Motif de refus"
        hint="Champ obligatoire pour valider l'action"
        placeholder="Sélectionner un motif de refus"
        required
        :options="motifs"
        :error="motifsUnavailable"
        error-message="Les motifs de refus n'ont pas pu être chargés."
      />
    </div>

    <template #footer>
      <div class="refus-candidature-dialog__footer">
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
      </div>
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

.refus-candidature-dialog__footer {
  display: flex;
  gap: var(--csp-space-3);
}
</style>
