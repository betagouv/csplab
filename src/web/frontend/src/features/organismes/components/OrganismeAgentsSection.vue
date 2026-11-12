<script setup lang="ts">
import type { Role } from '../types'
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
import { agentSearchKeys, formatAgentLabel, formatAgentName } from '@/features/agents/format'
import { pluralize } from '@/utils/format'
import { ORGANISME_AGENTS_COLUMNS } from '../columns'
import { useAddAgentToOrganisme } from '../composables/useAddAgentToOrganisme'
import { provideAgentActions } from '../composables/useAgentActions'
import { useOrganismeAgents } from '../composables/useOrganismeAgents'
import { ROLE_FIELD_LABEL, ROLE_LABELS, ROLE_OPTIONS } from '../constants/organisme'
import AttachAgentForm from './AttachAgentForm.vue'

const props = defineProps<{
  organismeUuid: string
}>()

const { agents, pending, error, revoke, revoking, changeRole, changingRole } = useOrganismeAgents(props.organismeUuid)
const { status, foundAgent, searching, search: searchAgent, add, submitting, reset } = useAddAgentToOrganisme(props.organismeUuid)
const { roleChange, revocation } = provideAgentActions()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const revocationDialogOpen = useRequestOpen(revocation)
const attachDrawerOpen = ref(false)
const roleDrawerOpen = useRequestOpen(roleChange)
const attachEmailError = ref('')

async function handleAdd(role: Role) {
  try {
    const agent = await add(role)
    addToast({
      variant: 'success',
      title: 'Utilisateur ajouté',
      description: `${formatAgentLabel(agent)} a rejoint l'organisme.`,
    })
    attachDrawerOpen.value = false
  }
  catch (submitError) {
    if (isHttpStatus(submitError, 409)) {
      attachEmailError.value = 'Cet utilisateur est déjà rattaché à l\'organisme.'
      return
    }
    addToast({ variant: 'error', title: 'L\'ajout de l\'utilisateur a échoué' })
  }
}

function resetAgentSearch(): void {
  attachEmailError.value = ''
  reset()
}

function openAttachDrawer(): void {
  resetAgentSearch()
  attachDrawerOpen.value = true
}

const rows = computed(() => agents.value ?? [])

const { search, filtered } = useTextSearch(rows, agentSearchKeys)

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'compte utilisateur', 'comptes utilisateurs')}`
})

async function handleRoleChange(role: Role): Promise<void> {
  const agent = roleChange.requested
  if (!agent) {
    return
  }
  try {
    await changeRole({ agent, role })
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatAgentName(agent)} est maintenant ${ROLE_LABELS[role].toLowerCase()}.`,
    })
    roleDrawerOpen.value = false
  }
  catch {
    addToast({ variant: 'error', title: 'La modification du rôle a échoué' })
  }
}

async function handleRevocation(): Promise<void> {
  if (!revocation.requested) {
    return
  }
  const agent = revocation.requested
  try {
    await revoke(agent)
    addToast({
      variant: 'success',
      title: 'Utilisateur révoqué',
      description: `${formatAgentName(agent)} n'a plus accès à l'organisme.`,
    })
    revocationDialogOpen.value = false
  }
  catch {
    addToast({ variant: 'error', title: 'La révocation a échoué' })
  }
}
</script>

<template>
  <section class="organisme-agents-section">
    <div class="organisme-agents-section__intro">
      <h2 class="organisme-agents-section__title">
        Comptes utilisateurs de l'organisme
      </h2>
      <p class="organisme-agents-section__description">
        Participent aux recrutements auxquels ils sont rattachés,
        selon les droits qui leur sont attribués.
      </p>
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des comptes utilisateurs"
      error-title="Impossible de charger les comptes utilisateurs"
    >
      <template #skeleton>
        <CspSkeletonTable
          :columns="ORGANISME_AGENTS_COLUMNS.length"
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspSearchBar
          v-model="search"
          mode="live"
          label="Rechercher une personne"
          hide-label
          placeholder="Rechercher une personne"
        />
        <CspButton
          label="Ajouter un utilisateur"
          icon="ri:user-add-line"
          is-icon-left
          @click="openAttachDrawer"
        />
      </CspTableToolbar>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="ORGANISME_AGENTS_COLUMNS"
        :row-key="row => row.uuid"
        caption="Comptes utilisateurs de l'organisme"
        :page-size="TABLE_PAGE_SIZE"
      >
        <template #empty>
          <div class="organisme-agents-section__empty">
            <template v-if="search">
              <p class="organisme-agents-section__empty-title">
                Aucun utilisateur ne correspond à votre recherche.
              </p>
            </template>
            <template v-else>
              <p class="organisme-agents-section__empty-title">
                Aucun utilisateur rattaché à l'organisme.
              </p>
            </template>
          </div>
        </template>
      </CspDataTable>
    </CspAsyncSection>

    <CspDrawer
      v-model:open="attachDrawerOpen"
      title="Ajouter un utilisateur"
      size="md"
    >
      <AttachAgentForm
        :status="status"
        :agent="foundAgent"
        :searching="searching"
        :submitting="submitting"
        :email-error="attachEmailError"
        @search="searchAgent"
        @add="handleAdd"
        @reset="resetAgentSearch"
        @cancel="attachDrawerOpen = false"
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
        :role="roleChange.requested.role"
        :role-label="ROLE_FIELD_LABEL"
        :options="ROLE_OPTIONS"
        :submitting="changingRole"
        @submit="handleRoleChange"
        @cancel="roleDrawerOpen = false"
      />
    </CspDrawer>

    <CspDialog
      v-model:open="revocationDialogOpen"
      title="Révoquer les accès"
      size="sm"
    >
      <template v-if="revocation.requested">
        {{ formatAgentName(revocation.requested) }} sera retiré de cet organisme et perdra
        immédiatement l'accès à ses recrutements. Son compte restera actif et pourra
        être rattaché à nouveau ultérieurement.
      </template>

      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="revocationDialogOpen = false"
        />
        <CspButton
          label="Révoquer les accès"
          :disabled="revoking"
          @click="handleRevocation"
        />
      </template>
    </CspDialog>
  </section>
</template>

<style scoped lang="scss">
.organisme-agents-section__intro {
  margin-bottom: var(--csp-space-5);
}

.organisme-agents-section__title {
  font-weight: 600;
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.organisme-agents-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  max-width: 65ch;
}

.organisme-agents-section__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) 0;
}

.organisme-agents-section__empty-title {
  margin: 0;
}
</style>
