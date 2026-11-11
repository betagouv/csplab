<script setup lang="ts">
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'

const VIEW_OPTIONS = [
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
  { value: 'tableau', label: 'Tableau', icon: 'ri:table-line' },
  { value: 'grille', label: 'Grille', icon: 'ri:layout-grid-line' },
]

const view = ref('liste')
</script>

<template>
  <div class="ecarts-controles">
    <CspSegmentedControl
      v-model="view"
      legend="Affichage"
      :options="VIEW_OPTIONS"
    />

    <div class="ecarts-controles__buttons">
      <CspButton label="Enregistrer" />
      <CspButton
        label="Annuler"
        variant="secondary"
      />
      <CspButton
        label="Trier par date"
        icon="ri:arrow-down-line"
        variant="tertiary"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.ecarts-controles {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
}

.ecarts-controles__buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-3);
}
</style>
