<script setup lang="ts">
import AtsAppShell from './components/AtsAppShell.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

const tabs = [
  { value: 'etapes', label: 'Gestion des étapes de recrutement' },
]
</script>

<template>
  <AtsAppShell>
    <div class="parametres-view">
      <header class="parametres-view__header">
        <h1 class="parametres-view__title">
          Paramètres de l'organisme
        </h1>
        <CspBadge icon="ri:building-line" label="Ministère de la Transition Écologique" />
      </header>

      <CspTabs :tabs="tabs" default-value="etapes">
        <template #etapes>
          <p>Contenu à venir</p>
        </template>
      </CspTabs>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.parametres-view {
  padding: 2rem;
}

.parametres-view__header {
  margin-bottom: 1.5rem;
}

.parametres-view__title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
