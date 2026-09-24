<script setup lang="ts">
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import MobileBottomSheet from '../../shared/mobile/MobileBottomSheet.vue'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirmer': [motif: string | undefined]
}>()

const motifs = [
  { value: 'Je ne suis plus disponible', label: 'Je ne suis plus disponible' },
  { value: 'Je ne suis plus intéressé·e par le poste', label: 'Je ne suis plus intéressé·e par le poste' },
  { value: 'J\'ai trouvé un autre poste', label: 'J\'ai trouvé un autre poste' },
  { value: 'Autre raison', label: 'Autre raison' },
]

const motif = ref('')

watch(() => props.open, (ouvert) => {
  if (ouvert) {
    motif.value = ''
  }
})
</script>

<template>
  <MobileBottomSheet
    :open="open"
    title="Retirer ma candidature ?"
    description="Cette action est définitive."
    @update:open="value => emit('update:open', value)"
  >
    <CspRadioGroup
      v-model="motif"
      label="Motif (facultatif)"
      name="motif-retrait"
      :options="motifs"
    />

    <template #footer>
      <CspButton
        variant="primary"
        size="lg"
        label="Retirer ma candidature"
        class="retrait__bouton"
        @click="emit('confirmer', motif || undefined)"
      />
      <CspButton
        variant="tertiary"
        size="lg"
        label="Annuler"
        class="retrait__bouton"
        @click="emit('update:open', false)"
      />
    </template>
  </MobileBottomSheet>
</template>

<style scoped lang="scss">
.retrait__bouton {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}
</style>
