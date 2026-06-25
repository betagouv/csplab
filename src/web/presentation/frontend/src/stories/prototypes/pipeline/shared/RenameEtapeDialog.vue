<script setup lang="ts">
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'

interface Props {
  open: boolean
  // Nom courant de l'étape éditée.
  nom: string
  // Noms déjà pris (pour interdire les doublons).
  noms: string[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': [nom: string]
}>()

const draft = ref(props.nom)
const error = ref<string | null>(null)

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    draft.value = props.nom
    error.value = null
  }
})

function validate(value: string): string | null {
  const trimmed = value.trim()
  if (!trimmed)
    return 'Le nom de l\'étape ne peut pas être vide.'
  if (trimmed !== props.nom && props.noms.includes(trimmed))
    return 'Une étape porte déjà ce nom.'
  return null
}

function confirm() {
  const message = validate(draft.value)
  if (message) {
    error.value = message
    return
  }
  emit('confirm', draft.value.trim())
  emit('update:open', false)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Renommer l'étape"
    close-label="Fermer"
    @update:open="value => emit('update:open', value)"
  >
    <CspInput
      v-model="draft"
      label="Nom de l'étape"
      :error="Boolean(error)"
      :error-message="error ?? undefined"
      @keydown.enter="confirm"
    />

    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        size="sm"
        @click="emit('update:open', false)"
      />
      <CspButton
        label="Valider"
        variant="primary"
        size="sm"
        @click="confirm"
      />
    </template>
  </CspDialog>
</template>
