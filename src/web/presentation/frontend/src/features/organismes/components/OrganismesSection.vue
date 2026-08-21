<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { pluralize } from '@/utils/format'
import { ORGANISMES_COLUMNS } from '../columns'
import { useOrganismes } from '../composables/useOrganismes'

const PAGE_SIZE = 8

const { organismes, pending, error } = useOrganismes()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)

const rows = computed(() => organismes.value ?? [])

const { search, filtered } = useTextSearch(rows, row => [row.nom, row.siret, row.gestionnaire])

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'organisme')}`
})
</script>

<template>
  <section class="organismes-section">
    <div class="organismes-section__intro">
      <div>
        <h2 class="organismes-section__title">
          Gestion des organismes
        </h2>
        <p class="organismes-section__description">
          Les organismes permettent d'organiser les recrutements. Chaque organisme
          dispose de ses propres utilisateurs, offres et paramètres.
        </p>
      </div>
      <CspButton
        label="Ajouter un organisme"
        icon="ri:add-line"
        is-icon-left
        disabled
      />
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des organismes"
      error-title="Impossible de charger les organismes"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="ORGANISMES_COLUMNS.length"
          with-footer
        />
      </template>

      <div class="organismes-section__header">
        <p class="organismes-section__count">
          {{ countLabel }}
        </p>
        <div class="organismes-section__actions">
          <CspInput
            v-model="search"
            type="search"
            aria-label="Rechercher un organisme, un siret"
            placeholder="Rechercher un organisme, un siret"
            class="organismes-section__search"
          />
        </div>
      </div>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="ORGANISMES_COLUMNS"
        :row-key="row => row.organisme_uuid"
        caption="Organismes"
        empty-label="Aucun organisme"
        :page-size="PAGE_SIZE"
      />
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.organismes-section__intro {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-6);
  margin-bottom: var(--csp-space-6);
}

.organismes-section__title {
  font-weight: 600;
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.organismes-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.organismes-section__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--csp-space-4);
}

.organismes-section__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.organismes-section__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.75rem;
  margin-bottom: var(--csp-space-4);
}

.organismes-section__search {
  min-width: 20rem;
}
</style>
