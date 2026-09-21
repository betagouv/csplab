<script setup lang="ts">
import type { EtapeRecrutement } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

const props = defineProps<{
  etapes: EtapeRecrutement[]
  currentEtapeUuid: string
}>()

const emit = defineEmits<{
  confirm: [targetEtapeUuid: string]
}>()

const open = ref(false)
const selectedEtapeUuid = ref('')

watch(open, () => {
  selectedEtapeUuid.value = ''
})

const options = computed(() => props.etapes.map((etape) => {
  const isCurrent = etape.etape_uuid === props.currentEtapeUuid
  return {
    value: etape.etape_uuid,
    label: isCurrent ? `${etape.nom} (étape actuelle)` : etape.nom,
    disabled: isCurrent,
  }
}))

function handleConfirm(): void {
  if (!selectedEtapeUuid.value)
    return
  emit('confirm', selectedEtapeUuid.value)
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
    <div class="changer-etape-popover">
      <CspRadioGroup
        v-model="selectedEtapeUuid"
        label="Nouvelle étape"
        name="etape"
        :options="options"
      />
      <CspButton
        label="Valider"
        size="sm"
        :disabled="!selectedEtapeUuid"
        @click="handleConfirm"
      />
    </div>
  </CspPopover>
</template>

<style scoped lang="scss">
.changer-etape-popover {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  align-items: flex-start;
}
</style>
