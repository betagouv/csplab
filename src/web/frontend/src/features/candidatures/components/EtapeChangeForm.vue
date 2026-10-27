<script setup lang="ts">
import type { EtapeRecrutement } from '../types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

const props = defineProps<{
  etapes: EtapeRecrutement[]
  currentEtapeUuid: string
}>()

const emit = defineEmits<{
  confirm: [targetEtapeUuid: string]
}>()

const selectedEtapeUuid = ref('')

const options = computed(() => props.etapes.map((etape) => {
  const isCurrent = etape.uuid === props.currentEtapeUuid
  return {
    value: etape.uuid,
    label: isCurrent ? `${etape.nom} (étape actuelle)` : etape.nom,
    disabled: isCurrent,
  }
}))

function handleConfirm(): void {
  if (selectedEtapeUuid.value) {
    emit('confirm', selectedEtapeUuid.value)
  }
}
</script>

<template>
  <div class="etape-change-form">
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
</template>

<style scoped lang="scss">
.etape-change-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  align-items: flex-start;
}
</style>
