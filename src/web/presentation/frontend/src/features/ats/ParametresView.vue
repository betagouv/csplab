<script setup lang="ts">
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import AtsAppShell from './components/AtsAppShell.vue'
import EtapesRecrutementList from './components/EtapesRecrutementList.vue'

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
        <CspBadge
          icon="ri:building-line"
          label="Ministère de la Transition Écologique"
        />
      </header>

      <CspTabs
        :tabs="tabs"
        default-value="etapes"
      >
        <template #etapes>
          <EtapesRecrutementList />
        </template>
      </CspTabs>
    </div>
  </AtsAppShell>
</template>

<style scoped lang="scss">
.parametres-view {
  padding: var(--csp-space-8);
}

.parametres-view__header {
  margin-bottom: var(--csp-space-6);
}

.parametres-view__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-2xl);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
