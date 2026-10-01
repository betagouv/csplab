<script setup lang="ts">
import type { CreateOrganismePayload, UpdateOrganismePayload } from '../types'
import { computed, ref, useTemplateRef, watch } from 'vue'
import { ValidationError } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { ORGANISMES_LIST_COLUMNS } from '../columns'
import { provideOrganismeEdition } from '../composables/useOrganismeEdition'
import { useOrganismes } from '../composables/useOrganismes'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

const PAGE_SIZE = 8

const { organismesList, pending, error, create, creating, update, updating } = useOrganismes()
const edition = provideOrganismeEdition()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const creationOpen = ref(false)

const drawerOpen = computed({
  get: () => creationOpen.value || edition.requested !== null,
  set: (value) => {
    if (!value) {
      creationOpen.value = false
      edition.clear()
    }
  },
})

const saving = computed(() => creating.value || updating.value)

const formDrawer = useTemplateRef('formDrawer')

const rows = computed(() => organismesList.value ?? [])

const { search, filtered } = useTextSearch(rows, row => [row.nom, row.siret, ...row.superviseurs.map(s => s.nom)])

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'organisme')}`
})

const { addToast } = useToast()

async function handleCreate(payload: CreateOrganismePayload): Promise<void> {
  try {
    await create(payload)
    addToast({ variant: 'success', title: 'Organisme créé' })
    drawerOpen.value = false
  }
  catch (submitError) {
    if (submitError instanceof ValidationError) {
      formDrawer.value?.setSiretError('Ce SIRET est déjà utilisé ou n\'est pas valide.')
      return
    }
    addToast({ variant: 'error', title: 'La création de l\'organisme a échoué' })
  }
}

async function handleUpdate(payload: UpdateOrganismePayload): Promise<void> {
  if (!edition.requested)
    return
  try {
    await update({ organismeUuid: edition.requested.organisme_uuid, payload })
    addToast({ variant: 'success', title: 'Organisme modifié' })
    drawerOpen.value = false
  }
  catch {
    addToast({ variant: 'error', title: 'La modification de l\'organisme a échoué' })
  }
}
</script>

<template>
  <section class="organismes-section">
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des organismes"
      error-title="Impossible de charger les organismes"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="ORGANISMES_LIST_COLUMNS.length"
          with-footer
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspSearchBar
          v-model="search"
          mode="live"
          label="Rechercher un organisme, un siret, un superviseur"
          hide-label
          placeholder="Rechercher un organisme, un siret, un superviseur"
          class="organismes-section__search"
        />
        <CspButton
          label="Ajouter un organisme"
          icon="ri:add-line"
          is-icon-left
          @click="creationOpen = true"
        />
      </CspTableToolbar>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="ORGANISMES_LIST_COLUMNS"
        :row-key="row => row.organisme_uuid"
        caption="Organismes"
        empty-label="Aucun organisme"
        :page-size="PAGE_SIZE"
      />
    </CspAsyncSection>

    <OrganismeFormDrawer
      ref="formDrawer"
      v-model:open="drawerOpen"
      :organisme="edition.requested"
      :saving="saving"
      @create="handleCreate"
      @update="handleUpdate"
    />
  </section>
</template>

<style scoped lang="scss">
.organismes-section__search {
  min-width: 20rem;
}
</style>
