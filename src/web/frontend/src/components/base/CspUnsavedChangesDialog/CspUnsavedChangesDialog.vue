<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  keepEditing: []
  leave: []
}>()
</script>

<template>
  <CspDialog
    :open="open"
    title="Modifications non enregistrées"
    @update:open="(value) => { if (!value) { emit('keepEditing') } }"
  >
    <p class="csp-unsaved-changes-dialog__text">
      Si vous quittez maintenant, votre saisie sera perdue.
    </p>

    <template #footer>
      <div class="csp-unsaved-changes-dialog__footer">
        <CspButton
          label="Quitter sans enregistrer"
          variant="secondary"
          @click="emit('leave')"
        />
        <CspButton
          label="Continuer l'édition"
          variant="primary"
          @click="emit('keepEditing')"
        />
      </div>
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.csp-unsaved-changes-dialog__text {
  margin: 0;
}

.csp-unsaved-changes-dialog__footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
