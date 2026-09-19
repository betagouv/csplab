<script setup lang="ts">
import type { Candidat } from '../types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import { formatCandidatNom } from '../utils/candidat'

const props = defineProps<{
  open: boolean
  candidat: Candidat | null
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const description = computed(() => {
  const candidatLabel = props.candidat ? formatCandidatNom(props.candidat) : 'ce candidat'
  return `Vous êtes sur le point de refuser la candidature de ${candidatLabel}. `
    + `Cette action n'est pas définitive, néanmoins le candidat sera informé du changement `
    + `de statut de sa candidature.`
})
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Refus de candidature"
    @update:open="(value) => { if (!value) emit('cancel') }"
  >
    {{ description }}

    <template #footer>
      <div class="refus-candidature-dialog__footer">
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="emit('cancel')"
        />
        <CspButton
          label="Valider"
          variant="primary"
          @click="emit('confirm')"
        />
      </div>
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.refus-candidature-dialog__footer {
  display: flex;
  gap: var(--csp-space-3);
}
</style>
