<script setup lang="ts">
import type { EtapeRecrutement } from '../types'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import EtapeChangeForm from './EtapeChangeForm.vue'

defineProps<{
  etapes: EtapeRecrutement[]
  currentEtapeUuid: string
}>()

const emit = defineEmits<{
  confirm: [targetEtapeUuid: string]
}>()

const open = ref(false)

function handleConfirm(targetEtapeUuid: string): void {
  emit('confirm', targetEtapeUuid)
  open.value = false
}
</script>

<template>
  <CspPopover
    v-model:open="open"
    side="bottom"
    align="end"
  >
    <template #trigger>
      <CspButton
        label="Changer d'étape"
        icon="ri:arrow-left-right-line"
        is-icon-left
        size="sm"
      />
    </template>
    <EtapeChangeForm
      :etapes="etapes"
      :current-etape-uuid="currentEtapeUuid"
      @confirm="handleConfirm"
    />
  </CspPopover>
</template>
