<script setup lang="ts">
import type { RecrutementRole } from '../types'
import { computed, ref } from 'vue'
import { isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useRequestOpen } from '@/composables/ui/useRequestOpen'
import { useToast } from '@/composables/ui/useToast'
import AgentRoleForm from '@/features/agents/components/AgentRoleForm.vue'
import { agentSearchKeys, formatAgentLabel } from '@/features/agents/format'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import { can } from '@/utils/authorizedActions'
import { pluralize } from '@/utils/format'
import { EQUIPE_RECRUTEMENT_ACTIONS_COLUMN, EQUIPE_RECRUTEMENT_COLUMNS } from '../columns'
import AddTeamMemberForm from '../components/AddTeamMemberForm.vue'
import MembreTagForm from '../components/MembreTagForm.vue'
import { useAddAgentToRecrutement } from '../composables/useAddAgentToRecrutement'
import { TagNotReplacedError, useEquipeRecrutement } from '../composables/useEquipeRecrutement'
import { provideMembreEquipeActions } from '../composables/useMembreEquipeActions'
import { RECRUTEMENT_ROLE_LABELS, RECRUTEMENT_ROLE_OPTIONS } from '../constants/equipe-recrutement'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const { membres, pending, error, revoke, revoking, changeRole, changingRole, changeTag, changingTag } = useEquipeRecrutement(
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
} = useAddAgentToRecrutement(props.organismeUuid, props.recrutementUuid)
const { recrutementDetail } = useRecrutementDetail(() => props)
const actions = computed(() => recrutementDetail.value?.authorized_actions)
const canAdd = computed(() => can(actions.value, 'add_recrutement_agent'))
const canChangeRole = computed(() => can(actions.value, 'update_recrutement_agent'))
const canRevoke = computed(() => can(actions.value, 'revoke_recrutement_agent'))
const canGrantResponsable = computed(() => can(actions.value, 'grant_recrutement_responsable'))
const roleOptions = computed(() =>
  canGrantResponsable.value
    ? RECRUTEMENT_ROLE_OPTIONS
    : RECRUTEMENT_ROLE_OPTIONS.filter(option => option.value !== 'responsable'),
)
const canChangeTag = computed(() => can(actions.value, 'manage_tag_on_member'))
const { revocation, roleChange, tagChange } = provideMembreEquipeActions({ canRevoke, canChangeRole, canChangeTag })
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const addMemberDrawerOpen = ref(false)
const addMemberEmailError = ref('')
const revocationDialogOpen = useRequestOpen(revocation)
const roleDrawerOpen = useRequestOpen(roleChange)
const tagDrawerOpen = useRequestOpen(tagChange)

const columns = computed(() =>
  canChangeRole.value || canChangeTag.value || canRevoke.value
    ? [...EQUIPE_RECRUTEMENT_COLUMNS, EQUIPE_RECRUTEMENT_ACTIONS_COLUMN]
    : EQUIPE_RECRUTEMENT_COLUMNS,
)

function resetAgentSearch(): void {
  addMemberEmailError.value = ''
  resetAgent()
}

function openAddMemberDrawer(): void {
  resetAgentSearch()
  addMemberDrawerOpen.value = true
}

async function handleAdd(role: RecrutementRole, tagUuid: string | null) {
  try {
    const membre = await add(role)
    addToast({
      variant: 'success',
      title: 'Membre ajouté',
      description: `${formatAgentLabel(membre)} a rejoint l'équipe de recrutement.`,
    })
    addMemberDrawerOpen.value = false
    if (tagUuid) {
      await changeTag({ membre, tagUuid }).catch(() => {
        addToast({ variant: 'error', title: 'L\'étiquette du membre n\'a pas pu être enregistrée' })
      })
    }
  }
  catch (submitError) {
    if (isHttpStatus(submitError, 409)) {
      addMemberEmailError.value = 'Cette personne fait déjà partie de l\'équipe.'
      return
    }
    addToast({ variant: 'error', title: 'L\'ajout du membre a échoué' })
  }
}

async function handleRoleChange(role: RecrutementRole): Promise<void> {
  const membre = roleChange.requested
  if (!membre) {
    return
  }
  try {
    await changeRole({ membre, role })
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatAgentLabel(membre)} est maintenant ${RECRUTEMENT_ROLE_LABELS[role].toLowerCase()} sur ce recrutement.`,
    })
    roleDrawerOpen.value = false
  }
  catch {
    addToast({ variant: 'error', title: 'La modification du rôle a échoué' })
  }
}

function tagChangeErrorTitle(tagError: unknown): string {
  if (tagError instanceof TagNotReplacedError) {
    return 'L\'ancienne étiquette a été retirée, mais la nouvelle n\'a pas pu être posée'
  }
  if (isHttpStatus(tagError, 404)) {
    return 'Ce membre ou cette étiquette n\'existe plus'
  }
  return 'La modification de l\'étiquette a échoué'
}

async function handleTagChange(tagUuid: string | null): Promise<void> {
  const membre = tagChange.requested
  if (!membre) {
    return
  }
  try {
    await changeTag({ membre, tagUuid })
    addToast({ variant: 'success', title: tagUuid ? 'Étiquette enregistrée' : 'Étiquette retirée' })
    tagDrawerOpen.value = false
  }
  catch (tagError) {
    addToast({ variant: 'error', title: tagChangeErrorTitle(tagError) })
  }
}

async function handleRevocation(): Promise<void> {
  if (!revocation.requested) {
    return
  }
  const membre = revocation.requested
  try {
    await revoke(membre)
    addToast({
      variant: 'success',
      title: 'Membre retiré',
      description: `${formatAgentLabel(membre)} ne fait plus partie de l'équipe de recrutement.`,
    })
    revocationDialogOpen.value = false
  }
  catch (revocationError) {
    const title = isHttpStatus(revocationError, 404)
      ? 'Cet agent ne fait plus partie de l\'équipe'
      : 'Le retrait du membre a échoué'
    addToast({ variant: 'error', title })
  }
}

const { search, filtered } = useTextSearch(membres, agentSearchKeys)

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
        des candidatures de ce recrutement.
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
          :columns="columns.length"
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspSearchBar
          v-model="search"
          mode="live"
          label="Rechercher un membre, un courriel"
          hide-label
          placeholder="Rechercher un membre, un courriel"
        />
        <CspButton
          v-if="canAdd"
          label="Ajouter un membre"
          icon="ri:user-add-line"
          is-icon-left
          @click="openAddMemberDrawer"
        />
      </CspTableToolbar>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="columns"
        :row-key="row => row.uuid"
        caption="Équipe de recrutement"
        :page-size="TABLE_PAGE_SIZE"
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

    <CspDrawer
      v-model:open="addMemberDrawerOpen"
      title="Ajouter un membre"
      size="md"
    >
      <AddTeamMemberForm
        :options="roleOptions"
        :status="agentStatus"
        :agent="foundAgent"
        :searching="searching"
        :submitting="submitting"
        :email-error="addMemberEmailError"
        :organisme-uuid="organismeUuid"
        :tags-editable="canChangeTag"
        @search="searchAgent"
        @add="handleAdd"
        @reset="resetAgentSearch"
        @cancel="addMemberDrawerOpen = false"
      />
    </CspDrawer>

    <CspDrawer
      v-model:open="roleDrawerOpen"
      title="Modifier les droits d'accès"
      size="md"
    >
      <AgentRoleForm
        v-if="roleChange.requested"
        :key="roleChange.requested.uuid"
        :email="roleChange.requested.email"
        :role="roleChange.requested.recrutement_role"
        role-label="Rôle dans le recrutement"
        :options="roleOptions"
        :submitting="changingRole"
        @submit="handleRoleChange"
        @cancel="roleDrawerOpen = false"
      />
    </CspDrawer>

    <CspDrawer
      v-model:open="tagDrawerOpen"
      title="Modifier l'étiquette"
      size="md"
    >
      <MembreTagForm
        v-if="tagChange.requested"
        :key="tagChange.requested.uuid"
        :organisme-uuid="organismeUuid"
        :email="tagChange.requested.email"
        :tag-uuid="tagChange.requested.tags[0]?.uuid ?? null"
        :submitting="changingTag"
        @submit="handleTagChange"
        @cancel="tagDrawerOpen = false"
      />
    </CspDrawer>

    <CspDialog
      v-model:open="revocationDialogOpen"
      title="Retirer de l’équipe"
      size="sm"
    >
      <template v-if="revocation.requested">
        {{ formatAgentLabel(revocation.requested) }} perdra l'accès aux candidatures de ce
        recrutement. Son compte reste rattaché à l'organisme et pourra être réintégré à
        l'équipe plus tard.
      </template>

      <template #footer>
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
</style>
