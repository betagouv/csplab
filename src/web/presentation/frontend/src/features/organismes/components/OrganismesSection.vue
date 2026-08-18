<script setup lang="ts">
import type { CreateOrganismePayload } from '../types'
import { computed, ref, useTemplateRef } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { ORGANISMES_COLUMNS } from '../columns'
import { useOrganismes } from '../composables/useOrganismes'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

const PAGE_SIZE = 8

const { organismes, pending, error, create, creating } = useOrganismes()
const { addToast } = useToast()

const page = ref(1)
const drawerOpen = ref(false)

const formDrawer = useTemplateRef('formDrawer')

const rows = computed(() => organismes.value ?? [])

const countLabel = computed(() => {
  const count = rows.value.length
  return `${count} ${pluralize(count, 'organisme')}`
})

async function handleSubmit(payload: CreateOrganismePayload): Promise<void> {
  try {
    await create(payload)
    addToast({ variant: 'success', title: 'Organisme créé' })
    drawerOpen.value = false
  }
  catch (submitError) {
    formDrawer.value?.setSiretConflict(submitError)
  }
}
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
        @click="drawerOpen = true"
      />
    </div>

    <CspAsyncSection
      :pending="pending"
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

      <p class="organismes-section__count">
        {{ countLabel }}
      </p>
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="ORGANISMES_COLUMNS"
        :row-key="row => row.uuid"
        caption="Organismes"
        empty-label="Aucun organisme"
        :page-size="PAGE_SIZE"
      />
    </CspAsyncSection>

    <OrganismeFormDrawer
      ref="formDrawer"
      v-model:open="drawerOpen"
      :saving="creating"
      @submit="handleSubmit"
    />
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
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.organismes-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.organismes-section__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}
</style>
