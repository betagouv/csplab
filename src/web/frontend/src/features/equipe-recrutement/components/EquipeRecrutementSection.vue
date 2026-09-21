<script setup lang="ts">
import type { RecrutementRole } from '../types'
import { computed, ref, useTemplateRef, watch } from 'vue'
import { HttpError } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useToast } from '@/composables/ui/useToast'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { pluralize } from '@/utils/format'
import { EQUIPE_RECRUTEMENT_ACTIONS_COLUMN, EQUIPE_RECRUTEMENT_COLUMNS } from '../columns'
import { useAjoutMembreEquipe } from '../composables/useAjoutMembreEquipe'
import { useEquipeRecrutement } from '../composables/useEquipeRecrutement'
import { useMembreEquipeActions } from '../composables/useMembreEquipeActions'
import { RECRUTEMENT_ROLE_LABELS } from '../constants/equipe-recrutement'
import { formatMembreLabel } from '../format'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const PAGE_SIZE = 8

const { membres, pending, error, revoke, revoking, changeRole } = useEquipeRecrutement(
  props.organismeUuid,
  props.recrutementUuid,
)
const {
  status: agentStatus,
  foundAgent,
  searching,
  search: searchAgent,
  add,
  submitting,
  reset: resetAgent,
} = useAjoutMembreEquipe(props.organismeUuid, props.recrutementUuid)
const { revocationMembre, clearRevocation, roleChange, clearRoleChange } = useMembreEquipeActions()
const { canManageOrganisme } = useRouteOrganisme()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const ajoutDrawerOpen = ref(false)
const ajoutDrawer = useTemplateRef('ajoutDrawer')
const revocationDialogOpen = ref(false)

const columns = computed(() =>
  canManageOrganisme.value
    ? [...EQUIPE_RECRUTEMENT_COLUMNS, EQUIPE_RECRUTEMENT_ACTIONS_COLUMN]
    : EQUIPE_RECRUTEMENT_COLUMNS,
)

async function handleSearchAgent(email: string) {
  try {
    await searchAgent(email)
  }
  catch {
    addToast({ variant: 'error', title: 'La recherche a échoué' })
  }
}

async function handleAdd(role: RecrutementRole) {
  try {
    const membre = await add(role)
    addToast({
      variant: 'success',
      title: 'Membre ajouté',
      description: `${formatMembreLabel(membre)} a rejoint l'équipe de recrutement.`,
    })
    ajoutDrawerOpen.value = false
  }
  catch (submitError) {
    if (submitError instanceof HttpError && submitError.status === 409) {
      ajoutDrawer.value?.setEmailError('Cette personne fait déjà partie de l\'équipe.')
      return
    }
    addToast({ variant: 'error', title: 'L\'ajout du membre a échoué' })
  }
}

watch(roleChange, async (change) => {
  if (!change)
    return
  const { membre, role } = change
  clearRoleChange()
  try {
    await changeRole({ membre, role })
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatMembreLabel(membre)} est maintenant ${RECRUTEMENT_ROLE_LABELS[role].toLowerCase()} sur ce recrutement.`,
    })
  }
  catch {
    addToast({ variant: 'error', title: 'La modification du rôle a échoué' })
  }
})

watch(revocationMembre, (membre) => {
  if (membre)
    revocationDialogOpen.value = true
})

watch(revocationDialogOpen, (isOpen) => {
  if (!isOpen)
    clearRevocation()
})

async function handleRevocation(): Promise<void> {
  if (!revocationMembre.value)
    return
  const membre = revocationMembre.value
  try {
    await revoke(membre)
    addToast({
      variant: 'success',
      title: 'Membre retiré',
      description: `${formatMembreLabel(membre)} ne fait plus partie de l'équipe de recrutement.`,
    })
    revocationDialogOpen.value = false
  }
  catch (revocationError) {
    const title = revocationError instanceof HttpError && revocationError.status === 404
      ? 'Cet agent ne fait plus partie de l\'équipe'
      : 'Le retrait du membre a échoué'
    addToast({ variant: 'error', title })
  }
}

const { search, filtered } = useTextSearch(membres, membre => [
  `${membre.prenom} ${membre.nom}`,
  `${membre.nom} ${membre.prenom}`,
  membre.email,
])

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'membre')}`
})
</script>

<template>
  <section class="equipe-recrutement-section">
    <div class="equipe-recrutement-section__intro">
      <h2 class="equipe-recrutement-section__title">
        Membres de l’équipe de recrutement
      </h2>
      <p class="equipe-recrutement-section__description">
        L'équipe de recrutement regroupe les utilisateurs qui participent au traitement
        des candidatures sur cette offre.
      </p>
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement de l'équipe de recrutement"
      error-title="Impossible de charger l'équipe de recrutement"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="columns.length"
          with-footer
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspSearchBar
          v-model="search"
          mode="live"
          label="Rechercher un membre, un courriel"
          hide-label
          placeholder="Rechercher un membre, un courriel"
          class="equipe-recrutement-section__search"
        />
        <CspButton
          v-if="canManageOrganisme"
          label="Ajouter un membre"
          icon="ri:user-add-line"
          is-icon-left
          @click="ajoutDrawerOpen = true"
        />
      </CspTableToolbar>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="columns"
        :row-key="row => row.agent_id"
        caption="Équipe de recrutement"
        :page-size="PAGE_SIZE"
      >
        <template #empty>
          <div class="equipe-recrutement-section__empty">
            <p class="equipe-recrutement-section__empty-title">
              <template v-if="search">
                Aucun membre ne correspond à votre recherche.
              </template>
              <template v-else>
                Aucun membre rattaché à ce recrutement.
              </template>
            </p>
          </div>
        </template>
      </CspDataTable>
    </CspAsyncSection>

    <AjoutMembreEquipeDrawer
      ref="ajoutDrawer"
      v-model:open="ajoutDrawerOpen"
      :status="agentStatus"
      :agent="foundAgent"
      :searching="searching"
      :submitting="submitting"
      @search="handleSearchAgent"
      @add="handleAdd"
      @reset="resetAgent"
    />

    <CspDialog
      v-model:open="revocationDialogOpen"
      title="Retirer de l’équipe"
      size="sm"
    >
      <template v-if="revocationMembre">
        {{ formatMembreLabel(revocationMembre) }} perdra l'accès aux candidatures de ce
        recrutement. Son compte reste rattaché à l'organisme et pourra être réintégré à
        l'équipe plus tard.
      </template>

      <template #footer>
        <div class="equipe-recrutement-section__dialog-actions">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="revocationDialogOpen = false"
          />
          <CspButton
            label="Retirer de l’équipe"
            :disabled="revoking"
            @click="handleRevocation"
          />
        </div>
      </template>
    </CspDialog>
  </section>
</template>

<style scoped lang="scss">
.equipe-recrutement-section__intro {
  margin-bottom: var(--csp-space-5);
}

.equipe-recrutement-section__title {
  font-weight: 600;
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.equipe-recrutement-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  max-width: 65ch;
}

.equipe-recrutement-section__search {
  min-width: 20rem;
}

.equipe-recrutement-section__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) 0;
}

.equipe-recrutement-section__empty-title {
  margin: 0;
}

.equipe-recrutement-section__dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
