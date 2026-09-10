<script setup lang="ts">
import type { ProtoAgent, RoleOrganisme } from '../data/mock'
import type { InvitationPayload, OrganismeTab } from '../shared/useEquipePrototype'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import type { CspMetaItem } from '@/components/base/CspMeta/types'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import ElapsedDaysCell from '@/components/base/CspDataTable/cells/ElapsedDaysCell.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { shortDate } from '@/utils/date'
import { pluralize } from '@/utils/format'
import ActiviteList from '../components/ActiviteList.vue'
import AjoutAgentOrganismeDrawer from '../components/AjoutAgentOrganismeDrawer.vue'
import AgentOrganismeActionsCell from '../components/cells/AgentOrganismeActionsCell.vue'
import MembreCell from '../components/cells/MembreCell.vue'
import RoleOrganismeCell from '../components/cells/RoleOrganismeCell.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { useMembreActions } from '../components/useMembreActions'
import { ORGANISME, ROLE_ORGANISME_LABELS } from '../data/mock'
import { useEquipePrototypeContext } from '../shared/context'
import { formatAgentNom, formatAgentNomAlphabetique } from '../shared/format'

const props = defineProps<{
  tab: OrganismeTab
}>()

const proto = useEquipePrototypeContext()
const { revocationDemande, annulerRevocation } = useMembreActions()

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: '/' },
  { label: 'Paramètres de l\'organisme' },
]

const TABS: CspTabItem<OrganismeTab>[] = [
  { value: 'membres', label: 'Membres', icon: 'ri:group-line' },
  { value: 'etapes', label: 'Étapes de recrutement', icon: 'ri:list-ordered' },
  { value: 'journal', label: 'Journal d\'audit', icon: 'ri:history-line' },
]

const PAGE_SIZE = 8

const META: CspMetaItem[] = [{ icon: 'ri:government-line', label: ORGANISME, srLabel: 'Organisme' }]

const activeTab = computed({
  get: () => props.tab,
  set: (tab) => {
    proto.page.value = { name: 'parametres-organisme', tab }
  },
})

const showSkeleton = useMinimumPending(proto.pending)

const COLUMNS: CspColumnDef<ProtoAgent>[] = [
  { id: 'agent', header: 'Membre', sortable: true, width: '14rem', accessor: row => formatAgentNomAlphabetique(row), cellComponent: MembreCell },
  { id: 'role', header: 'Rôle', sortable: true, width: '9rem', accessor: row => ROLE_ORGANISME_LABELS[row.roleOrganisme], cellComponent: RoleOrganismeCell },
  { id: 'poste', header: 'Poste', width: '12rem', accessor: row => row.poste },
  { id: 'email', header: 'Courriel', accessor: row => row.email },
  { id: 'derniereActivite', header: 'Dernière activité', sortable: true, width: '9rem', wrapHeader: true, accessor: row => row.dateDerniereActivite, cellComponent: ElapsedDaysCell },
  { id: 'dateCreation', header: 'Création de compte', width: '9rem', wrapHeader: true, accessor: row => shortDate.format(new Date(row.dateCreation)) },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: AgentOrganismeActionsCell },
]

const rows = computed(() => proto.scenario.agents)

const { search, filtered } = useTextSearch(rows, row => [
  formatAgentNom(row),
  formatAgentNomAlphabetique(row),
  row.email,
  row.poste,
])

const page = ref(1)

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'membre')}`
})

const ajoutOpen = ref(false)

function handleAjout(invitation: InvitationPayload, roleOrganisme: RoleOrganisme): void {
  proto.inviterALaVolee(invitation, null, roleOrganisme)
  ajoutOpen.value = false
}

const revocationOpen = computed({
  get: () => revocationDemande.value !== null,
  set: (open) => {
    if (!open)
      annulerRevocation()
  },
})

const offresDuRevoque = computed(() => {
  const agent = revocationDemande.value
  if (!agent)
    return 0
  return proto.scenario.recrutements.filter(r => r.membres.some(m => m.agentUuid === agent.uuid)).length
})

function confirmerRevocation(): void {
  const agent = revocationDemande.value
  if (!agent)
    return
  proto.revoquer(agent.uuid)
  annulerRevocation()
}
</script>

<template>
  <CspPageHeader
    title="Paramètres de l'organisme"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <CspMetaList :items="META" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    :tabs="TABS"
  >
    <template #tab-membres>
      <section class="organisme-section">
        <div class="organisme-section__intro">
          <h2 class="organisme-section__title">
            Membres de l'organisme
          </h2>
          <p class="organisme-section__description">
            Participent aux recrutements sur les offres auxquelles ils sont rattachés, selon les droits qui leur sont attribués.
            <template v-if="!proto.isAdmin.value">
              Seul l'administrateur de la plateforme peut promouvoir un membre gestionnaire.
            </template>
          </p>
        </div>

        <CspAsyncSection
          :pending="showSkeleton"
          loading-label="Chargement des membres"
        >
          <template #skeleton>
            <CspSkeletonTable
              :rows="PAGE_SIZE"
              :columns="COLUMNS.length"
              with-footer
            />
          </template>

          <CspTableToolbar :count="countLabel">
            <CspInput
              v-model="search"
              type="search"
              aria-label="Rechercher un membre, un courriel"
              placeholder="Rechercher un membre, un courriel"
              class="organisme-section__search"
            />
            <CspButton
              label="Créer un compte"
              icon="ri:user-add-line"
              is-icon-left
              @click="ajoutOpen = true"
            />
          </CspTableToolbar>
          <CspDataTable
            v-model:page="page"
            :rows="filtered"
            :columns="COLUMNS"
            :row-key="row => row.uuid"
            caption="Membres de l'organisme"
            :page-size="PAGE_SIZE"
          >
            <template #empty>
              <CspEmptyState
                :title="search ? 'Aucun membre ne correspond à votre recherche.' : 'Aucun membre pour l\'instant.'"
                icon="ri:group-line"
              />
            </template>
          </CspDataTable>
        </CspAsyncSection>
      </section>
    </template>

    <template #tab-etapes>
      <CspEmptyState
        title="Étapes de recrutement de l'organisme"
        description="Le paramétrage des étapes est celui de l'application actuelle et ne fait pas partie de ce prototype."
        icon="ri:list-ordered"
      />
    </template>

    <template #tab-journal>
      <section class="organisme-section">
        <div class="organisme-section__intro">
          <h2 class="organisme-section__title">
            Journal d'audit
          </h2>
          <p class="organisme-section__description">
            Créations de compte, changements de rôle et révocations, du plus récent au plus ancien.
          </p>
        </div>
        <ActiviteList
          :evenements="proto.journalOrganisme.value"
          empty-title="Aucune action enregistrée."
        />
      </section>
    </template>
  </CspPageContainer>

  <AjoutAgentOrganismeDrawer
    v-model:open="ajoutOpen"
    @submit="handleAjout"
  />

  <ConfirmDialog
    v-model:open="revocationOpen"
    title="Révoquer les accès"
    confirm-label="Révoquer les accès"
    confirm-icon="ri:user-unfollow-line"
    @confirm="confirmerRevocation"
  >
    <template v-if="revocationDemande">
      {{ formatAgentNom(revocationDemande) }} perdra immédiatement l'accès à l'organisme
      <template v-if="offresDuRevoque > 0">
        et sera retiré de {{ offresDuRevoque }} {{ pluralize(offresDuRevoque, 'équipe') }} de recrutement
      </template>.
      Cette action est tracée dans le journal d'audit.
    </template>
  </ConfirmDialog>
</template>

<style scoped lang="scss">
.organisme-section__intro {
  margin-bottom: var(--csp-space-5);
}

.organisme-section__title {
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
  font-weight: 600;
}

.organisme-section__description {
  margin: 0;
  max-width: 65ch;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.organisme-section__search {
  min-width: 20rem;
}
</style>
