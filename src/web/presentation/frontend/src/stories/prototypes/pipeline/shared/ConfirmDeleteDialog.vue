<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

interface Props {
  open: boolean
  // Nom de l'étape à supprimer, pour le rappeler dans le message.
  nom: string
}

defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': []
}>()

function confirm() {
  emit('confirm')
  emit('update:open', false)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Supprimer l'étape"
    close-label="Fermer"
    @update:open="value => emit('update:open', value)"
  >
    <p class="confirm__text">
      Supprimer l'étape <strong>« {{ nom }} »</strong> ? Elle sera retirée du
      pipeline. Cette action reste réversible tant que les modifications ne sont
      pas enregistrées.
    </p>

    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        size="sm"
        @click="emit('update:open', false)"
      />
      <CspButton
        class="confirm__delete"
        label="Supprimer"
        variant="primary"
        size="sm"
        @click="confirm"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.confirm__text {
  margin: 0;
}

// Bouton destructif : on teinte en rouge le primary du dialog.
.confirm__delete {
  background-color: var(--background-action-high-error);

  &:hover {
    background-color: var(--background-action-high-error-hover);
  }

  &:active {
    background-color: var(--background-action-high-error-active);
  }
}
</style>
