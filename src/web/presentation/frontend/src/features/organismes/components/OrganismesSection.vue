<script setup lang="ts">
import type { CreateCompteUtilisateurPayload, CreateOrganismePayload, UtilisateurRecherche } from '../types'
import { computed, ref, useTemplateRef, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { ORGANISMES_COLUMNS } from '../columns'
import { useGestionnaireAssignation } from '../composables/useGestionnaireAssignation'
import { useOrganismeEdition } from '../composables/useOrganismeEdition'
import { useOrganismes } from '../composables/useOrganismes'
import GestionnaireAssignDrawer from './GestionnaireAssignDrawer.vue'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

const PAGE_SIZE = 8

const { organismes, pending, error, create, creating, update, updating, assign, assigning, createCompte, creatingCompte } = useOrganismes()
const { editedOrganisme, closeEdition } = useOrganismeEdition()
const { assignationOrganisme, closeAssignation } = useGestionnaireAssignation()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const drawerOpen = ref(false)
const assignDrawerOpen = ref(false)

const formDrawer = useTemplateRef('formDrawer')

watch(editedOrganisme, (organisme) => {
  if (organisme)
    drawerOpen.value = true
})

watch(drawerOpen, (isOpen) => {
  if (!isOpen)
    closeEdition()
})

watch(assignationOrganisme, (organisme) => {
  if (organisme)
    assignDrawerOpen.value = true
})

watch(assignDrawerOpen, (isOpen) => {
  if (!isOpen)
    closeAssignation()
})

const rows = computed(() => organismes.value ?? [])

const countLabel = computed(() => {
  const count = rows.value.length
  return `${count} ${pluralize(count, 'organisme')}`
})

const saving = computed(() => creating.value || updating.value)

async function handleSubmit(payload: CreateOrganismePayload): Promise<void> {
  try {
    if (editedOrganisme.value) {
      const { siret: _siret, ...updatePayload } = payload
      await update({ uuid: editedOrganisme.value.uuid, payload: updatePayload })
      addToast({ variant: 'success', title: 'Organisme modifié' })
    }
    else {
      await create(payload)
      addToast({ variant: 'success', title: 'Organisme créé' })
    }
    drawerOpen.value = false
  }
  catch (submitError) {
    formDrawer.value?.setSiretConflict(submitError)
  }
}

async function handleAssign(utilisateur: UtilisateurRecherche): Promise<void> {
  if (!assignationOrganisme.value)
    return
  await assign({ uuid: assignationOrganisme.value.uuid, utilisateur })
  addToast({ variant: 'success', title: 'Gestionnaire assigné' })
  assignDrawerOpen.value = false
}

async function handleCreateCompte(payload: CreateCompteUtilisateurPayload): Promise<void> {
  if (!assignationOrganisme.value)
    return
  await createCompte({ uuid: assignationOrganisme.value.uuid, payload })
  addToast({
    variant: 'success',
    title: 'Compte créé et gestionnaire assigné',
    description: `Une invitation a été envoyée à ${payload.email}`,
  })
  assignDrawerOpen.value = false
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
      :organisme="editedOrganisme"
      :saving="saving"
      @submit="handleSubmit"
    />

    <GestionnaireAssignDrawer
      v-model:open="assignDrawerOpen"
      :organisme="assignationOrganisme"
      :saving="assigning || creatingCompte"
      @assign="handleAssign"
      @create="handleCreateCompte"
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
