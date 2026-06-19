<script setup lang="ts">
import type { EtapeRecrutement } from '../api/recrutement'
import { onMounted, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { getEtapesRecrutement } from '../api/recrutement'
import EtapesRecrutementListItem from './EtapesRecrutementListItem.vue'

const etapes = ref<EtapeRecrutement[]>([])
const loading = ref(true)
const error = ref<Error | null>(null)

const TEMP_ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

onMounted(async () => {
  try {
    etapes.value = await getEtapesRecrutement(TEMP_ORGANISME_UUID)
  }
  catch (err) {
    error.value = err instanceof Error ? err : new Error(String(err))
  }
  finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="etapes-list">
    <header class="etapes-list__header">
      <h2 class="etapes-list__title">
        Étapes de recrutement
      </h2>
      <CspButton
        label="Ajouter une étape"
        icon="ri:add-line"
        variant="secondary"
        is-icon-left
      />
    </header>

    <div
      v-if="loading"
      class="etapes-list__loading"
    >
      Chargement...
    </div>

    <div
      v-else-if="error"
      class="etapes-list__error"
    >
      Une erreur est survenue lors du chargement des étapes.
    </div>

    <div
      v-else
      class="etapes-list__content"
    >
      <div class="etapes-list__labels">
        <span class="etapes-list__label etapes-list__label--ordre">Ordre</span>
        <span class="etapes-list__label etapes-list__label--nom">Nom de l'étape</span>
        <span class="etapes-list__label etapes-list__label--type">Type d'étape</span>
      </div>

      <EtapesRecrutementListItem
        v-for="(etape, index) in etapes"
        :key="etape.etape_uuid"
        :etape="etape"
        :ordre="index + 1"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.etapes-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--csp-space-6);
}

.etapes-list__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.etapes-list__loading,
.etapes-list__error {
  padding: var(--csp-space-4);
  color: var(--text-mention-grey);
}

.etapes-list__error {
  color: var(--text-default-error);
}

.etapes-list__labels {
  display: grid;
  grid-template-columns: 2.5rem 4.5rem 1fr 12rem 2.5rem;
  gap: var(--csp-space-3);
  padding-bottom: var(--csp-space-2);
  margin-bottom: var(--csp-space-2);
}

.etapes-list__label {
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-mention-grey);
}

.etapes-list__label--ordre {
  grid-column: 2;
}

.etapes-list__label--nom {
  grid-column: 3;
}

.etapes-list__label--type {
  grid-column: 4;
}
</style>
