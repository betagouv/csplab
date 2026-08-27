<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { ORGANISME_AGENTS_COLUMNS } from '../columns'
import { useAgentActions } from '../composables/useAgentActions'
import { useOrganismeAgents } from '../composables/useOrganismeAgents'
import { ROLE_LABELS } from '../constants/organisme'
import { formatAgentName } from '../format'

const props = defineProps<{
  organismeUuid: string
}>()

const PAGE_SIZE = 8

const { agents, pending, error, updateAgent, updatingAgent } = useOrganismeAgents(props.organismeUuid)
const { roleChange, clearRoleChange, revocationAgent, clearRevocation } = useAgentActions()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const revocationDialogOpen = ref(false)

const rows = computed(() => agents.value ?? [])

const { search, filtered } = useTextSearch(rows, row => [
  `${row.prenom} ${row.nom}`,
  `${row.nom} ${row.prenom}`,
  row.email,
])

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'membre')}`
})

watch(roleChange, async (change) => {
  if (!change)
    return
  const { agent, role } = change
  clearRoleChange()
  try {
    await updateAgent({ agent_id: agent.agent_id, role })
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatAgentName(agent)} est maintenant ${ROLE_LABELS[role].toLowerCase()}.`,
    })
  }
  catch {
    addToast({ variant: 'error', title: 'La modification du rôle a échoué' })
  }
})

watch(revocationAgent, (agent) => {
  if (agent)
    revocationDialogOpen.value = true
})

watch(revocationDialogOpen, (isOpen) => {
  if (!isOpen)
    clearRevocation()
})

async function handleRevocation(): Promise<void> {
  if (!revocationAgent.value)
    return
  const agent = revocationAgent.value
  try {
    await updateAgent({ agent_id: agent.agent_id, date_revocation: new Date().toISOString() })
    addToast({
      variant: 'success',
      title: 'Membre révoqué',
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
        Membres de l'organisme
      </h2>
      <p class="organisme-agents-section__description">
        Participent aux recrutements sur les offres auxquelles ils sont rattachés,
        selon les droits qui leur sont attribués.
      </p>
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des membres"
      error-title="Impossible de charger les membres"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="ORGANISME_AGENTS_COLUMNS.length"
          with-footer
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspInput
          v-model="search"
          type="search"
          aria-label="Rechercher un membre, un courriel"
          placeholder="Rechercher un membre, un courriel"
          class="organisme-agents-section__search"
        />
      </CspTableToolbar>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="ORGANISME_AGENTS_COLUMNS"
        :row-key="row => row.agent_id"
        caption="Membres de l'organisme"
        :page-size="PAGE_SIZE"
      >
        <template #empty>
          <div class="organisme-agents-section__empty">
            <template v-if="search">
              <p class="organisme-agents-section__empty-title">
                Aucun membre ne correspond à votre recherche.
              </p>
            </template>
            <template v-else>
              <p class="organisme-agents-section__empty-title">
                Aucun membre pour l'instant.
              </p>
            </template>
          </div>
        </template>
      </CspDataTable>
    </CspAsyncSection>

    <CspDialog
      v-model:open="revocationDialogOpen"
      title="Révoquer les accès"
      size="sm"
    >
      <template v-if="revocationAgent">
        {{ formatAgentName(revocationAgent) }} sera retiré de cet organisme et perdra
        immédiatement l'accès à ses recrutements. Son compte restera actif et pourra
        être rattaché à nouveau ultérieurement.
      </template>

      <template #footer>
        <div class="organisme-agents-section__dialog-actions">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="revocationDialogOpen = false"
          />
          <CspButton
            label="Révoquer les accès"
            :disabled="updatingAgent"
            @click="handleRevocation"
          />
        </div>
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

.organisme-agents-section__search {
  min-width: 20rem;
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

.organisme-agents-section__dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
