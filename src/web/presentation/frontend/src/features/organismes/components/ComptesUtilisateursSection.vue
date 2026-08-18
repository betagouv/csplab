<script setup lang="ts">
import type { CompteUtilisateur, CreateCompteUtilisateurPayload } from '../types'
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { COMPTES_UTILISATEURS_COLUMNS } from '../columns'
import { useComptesUtilisateurs } from '../composables/useComptesUtilisateurs'
import { useResendInvitation } from '../composables/useResendInvitation'
import CompteUtilisateurForm from './CompteUtilisateurForm.vue'

const props = defineProps<{
  organismeUuid: string
}>()

const PAGE_SIZE = 8

const { comptes, pending, error, create, creating, resend, resending }
  = useComptesUtilisateurs(props.organismeUuid)
const { resendCompte, closeResend } = useResendInvitation()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const search = ref('')
const drawerOpen = ref(false)
const resendDialogOpen = ref(false)

watch(resendCompte, (compte) => {
  if (compte)
    resendDialogOpen.value = true
})

watch(resendDialogOpen, (isOpen) => {
  if (!isOpen)
    closeResend()
})

watch(search, () => {
  page.value = 1
})

const rows = computed(() => {
  const all = comptes.value ?? []
  const term = search.value.trim().toLowerCase()
  if (!term)
    return all
  return all.filter((compte: CompteUtilisateur) =>
    `${compte.prenom} ${compte.nom}`.toLowerCase().includes(term)
    || compte.email.toLowerCase().includes(term),
  )
})

const countLabel = computed(() => {
  const count = rows.value.length
  return `${count} ${pluralize(count, 'compte utilisateur', 'comptes utilisateurs')}`
})

async function handleCreate(payload: CreateCompteUtilisateurPayload): Promise<void> {
  await create(payload)
  addToast({
    variant: 'success',
    title: 'Compte créé',
    description: `Une invitation a été envoyée à ${payload.email}`,
  })
  drawerOpen.value = false
}

async function handleResend(): Promise<void> {
  if (!resendCompte.value)
    return
  const email = resendCompte.value.email
  await resend(resendCompte.value.uuid)
  addToast({ variant: 'success', title: `Invitation renvoyée à ${email}` })
  resendDialogOpen.value = false
}
</script>

<template>
  <section class="comptes-section">
    <div class="comptes-section__intro">
      <div>
        <h2 class="comptes-section__title">
          Utilisateurs de l'organisme
        </h2>
        <p class="comptes-section__description">
          Participent aux recrutements sur les offres auxquelles ils sont rattachés,
          selon les droits qui leur sont attribués.
        </p>
      </div>
      <CspButton
        label="Ajouter un compte"
        icon="ri:add-line"
        is-icon-left
        @click="drawerOpen = true"
      />
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des comptes utilisateurs"
      error-title="Impossible de charger les comptes utilisateurs"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="COMPTES_UTILISATEURS_COLUMNS.length"
          with-footer
        />
      </template>

      <div class="comptes-section__toolbar">
        <p class="comptes-section__count">
          {{ countLabel }}
        </p>
        <CspInput
          v-model="search"
          type="search"
          label="Rechercher une personne ou un mail"
          name="search"
          class="comptes-section__search"
        />
      </div>
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="COMPTES_UTILISATEURS_COLUMNS"
        :row-key="row => row.uuid"
        caption="Comptes utilisateurs"
        empty-label="Aucun compte utilisateur"
        :page-size="PAGE_SIZE"
      />
    </CspAsyncSection>

    <CspDrawer
      v-model:open="drawerOpen"
      title="Créer un compte"
      size="md"
    >
      <CompteUtilisateurForm
        submit-label="Créer le compte"
        :saving="creating"
        @submit="handleCreate"
        @cancel="drawerOpen = false"
      />
    </CspDrawer>

    <CspDialog
      v-model:open="resendDialogOpen"
      title="Renvoyer une invitation"
      :description="resendCompte ? `Un nouveau courriel d'invitation sera envoyé à ${resendCompte.email}. Le lien précédent sera invalidé.` : undefined"
      size="sm"
    >
      <div class="comptes-section__dialog-actions">
        <CspButton
          label="Renvoyer l'invitation"
          :disabled="resending"
          @click="handleResend"
        />
        <CspButton
          variant="secondary"
          label="Annuler"
          @click="resendDialogOpen = false"
        />
      </div>
    </CspDialog>
  </section>
</template>

<style scoped lang="scss">
.comptes-section__intro {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-6);
  margin-bottom: var(--csp-space-6);
}

.comptes-section__title {
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.comptes-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.comptes-section__toolbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--csp-space-4);
  margin-bottom: var(--csp-space-4);
}

.comptes-section__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.comptes-section__search {
  width: 20rem;
}

.comptes-section__dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-4);
}
</style>
