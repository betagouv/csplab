<script setup lang="ts">
import { ref } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

const FORMAT_OPTIONS = [
  { value: 'csv', label: 'CSV' },
  { value: 'pdf', label: 'PDF' },
]

const SORT_OPTIONS = [
  { value: 'date', label: 'Date de création' },
  { value: 'nom', label: 'Nom' },
]

const name = ref('')
const comment = ref('')
const sort = ref<string>()
const copy = ref(false)
const remember = ref(true)
const format = ref('csv')
</script>

<template>
  <div class="ecarts-cases">
    <div class="ecarts-cases__column">
      <CspCheckbox
        v-model="copy"
        label="Recevoir une copie par courriel"
      />
      <CspCheckbox
        v-model="remember"
        label="Se souvenir de moi"
      />
      <CspRadioGroup
        v-model="format"
        label="Format d'export"
        :options="FORMAT_OPTIONS"
      />
    </div>

    <div class="ecarts-cases__column">
      <CspInput
        v-model="name"
        label="Nom"
      />
      <CspSelect
        v-model="sort"
        label="Trier par"
        :options="SORT_OPTIONS"
      />
      <CspTextarea
        v-model="comment"
        label="Commentaire"
        :rows="3"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.ecarts-cases {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
}

.ecarts-cases__column {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}
</style>
