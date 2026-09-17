<script setup lang="ts">
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

export interface ReponsesQualification {
  titulaireFp: string
  disponibleSeptembre: string
  permisB: string
}

withDefaults(defineProps<{
  showIntro?: boolean
}>(), {
  showIntro: true,
})

const model = defineModel<ReponsesQualification>({
  default: () => ({ titulaireFp: '', disponibleSeptembre: '', permisB: '' }),
})

const ouiNon = [
  { value: 'oui', label: 'Oui' },
  { value: 'non', label: 'Non' },
]
</script>

<template>
  <div class="questions">
    <p
      v-if="showIntro"
      class="questions__intro"
    >
      Quelques questions courtes, propres à cette offre. Cela ne prend qu'une minute.
    </p>

    <CspRadioGroup
      v-model="model.titulaireFp"
      label="Êtes-vous titulaire de la fonction publique ?"
      name="titulaire-fp"
      :options="ouiNon"
    />

    <CspRadioGroup
      v-model="model.disponibleSeptembre"
      label="Êtes-vous disponible à partir de septembre ?"
      name="disponible-septembre"
      :options="ouiNon"
    />

    <CspRadioGroup
      v-model="model.permisB"
      label="Possédez-vous le permis B ?"
      name="permis-b"
      :options="ouiNon"
    />
  </div>
</template>

<style scoped lang="scss">
.questions {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.questions__intro {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}
</style>
