<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

withDefaults(defineProps<{
  title: string
  confirmLabel: string
  confirmIcon?: string
}>(), {
  confirmIcon: undefined,
})

const emit = defineEmits<{
  confirm: []
}>()

const open = defineModel<boolean>('open', { required: true })
</script>

<template>
  <CspDialog
    v-model:open="open"
    :title="title"
    size="sm"
  >
    <slot />
    <template #footer>
      <div class="confirm-dialog__actions">
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="open = false"
        />
        <CspButton
          :label="confirmLabel"
          :icon="confirmIcon"
          :is-icon-left="Boolean(confirmIcon)"
          @click="emit('confirm')"
        />
      </div>
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.confirm-dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
