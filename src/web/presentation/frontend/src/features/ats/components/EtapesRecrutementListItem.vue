<script setup lang="ts">
import type { EtapeRecrutement } from '../api/recrutement'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'

interface Props {
  etape: EtapeRecrutement
  ordre: number
}

const props = defineProps<Props>()

const nom = ref(props.etape.nom)

watch(() => props.etape.nom, (value) => {
  nom.value = value
})

const categorieOptions = [
  { value: 'INITIALE', label: 'Nouvelle' },
  { value: 'EN_COURS', label: 'En cours' },
  { value: 'TERMINALE', label: 'Étape finale' },
]

const isLocked = computed(() =>
  props.etape.categorie === 'INITIALE' || props.etape.categorie === 'TERMINALE',
)
</script>

<template>
  <div class="etape-item">
    <div class="etape-item__cell etape-item__cell--drag">
      <CspIcon
        v-if="!isLocked"
        name="ri:draggable"
        :size="16"
        class="etape-item__drag-icon"
      />
      <CspIcon
        v-else
        name="ri:lock-line"
        :size="16"
        class="etape-item__lock-icon"
      />
    </div>

    <div class="etape-item__cell etape-item__cell--ordre">
      <CspInput
        :model-value="String(ordre)"
        disabled
      />
    </div>

    <div class="etape-item__cell etape-item__cell--nom">
      <CspInput v-model="nom" />
    </div>

    <div class="etape-item__cell etape-item__cell--type">
      <CspSelect
        :model-value="etape.categorie"
        :options="categorieOptions"
        disabled
      />
    </div>

    <div class="etape-item__cell etape-item__cell--actions">
      <CspButton
        v-if="!isLocked"
        icon="ri:delete-bin-line"
        variant="tertiary-no-outline"
        size="sm"
        disabled
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.etape-item {
  display: grid;
  grid-template-columns: 2.5rem 4.5rem 1fr 12rem 2.5rem;
  gap: var(--csp-space-3);
  align-items: center;
  padding: var(--csp-space-2) 0;
}

.etape-item__cell--drag {
  display: flex;
  justify-content: center;
}

.etape-item__drag-icon {
  color: var(--text-mention-grey);
  cursor: grab;
}

.etape-item__lock-icon {
  color: var(--text-mention-grey);
}

.etape-item__cell--type {
  width: 100%;
}

.etape-item__cell--actions {
  display: flex;
  justify-content: center;
}
</style>
