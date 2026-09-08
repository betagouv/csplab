<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  continuer: []
  quitter: []
}>()
</script>

<template>
  <CspDialog
    :open="open"
    size="sm"
    title="Modifications non enregistrées"
    description="Si vous quittez maintenant, votre saisie sera perdue."
    close-label="Continuer l'édition"
    @update:open="(value) => { if (!value) emit('continuer') }"
  >
    <template #footer>
      <div class="garde-fou__footer">
        <CspButton
          label="Quitter sans enregistrer"
          variant="secondary"
          @click="emit('quitter')"
        />
        <CspButton
          label="Continuer l'édition"
          @click="emit('continuer')"
        />
      </div>
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.garde-fou__footer {
  display: flex;
  gap: var(--csp-space-3);
}
</style>
