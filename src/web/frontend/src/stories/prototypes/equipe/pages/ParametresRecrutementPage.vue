<script setup lang="ts">
import type { AjoutMembreResultat } from '../components/AjoutMembreDrawer.vue'
import type { ProtoAgent, ProtoMembre } from '../data/mock'
import type { RecrutementTab } from '../shared/useEquipePrototype'
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
import AjoutMembreDrawer from '../components/AjoutMembreDrawer.vue'
import MembreActionsCell from '../components/cells/MembreActionsCell.vue'
import MembreCell from '../components/cells/MembreCell.vue'
import RoleOffreCell from '../components/cells/RoleOffreCell.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { useMembreActions } from '../components/useMembreActions'
import { ROLE_OFFRE_LABELS } from '../data/mock'
import { useEquipePrototypeContext } from '../shared/context'
import { formatAgentNom, formatAgentNomAlphabetique } from '../shared/format'

const props = defineProps<{
  recrutementUuid: string
  tab: RecrutementTab
}>()

const proto = useEquipePrototypeContext()
const { retraitDemande, annulerRetrait } = useMembreActions()

interface MembreRow {
  agent: ProtoAgent
  membre: ProtoMembre
  recrutementUuid: string
}

const TABS: CspTabItem<RecrutementTab>[] = [
  { value: 'equipe', label: 'Équipe de recrutement', icon: 'ri:team-line' },
  { value: 'etapes', label: 'Étapes de recrutement', icon: 'ri:list-ordered' },
  { value: 'activite', label: 'Activité', icon: 'ri:history-line' },
]

const PAGE_SIZE = 8

const recrutement = computed(() => proto.recrutementOf(props.recrutementUuid))
const peutGerer = computed(() => proto.peutGererEquipe(props.recrutementUuid))
const estResponsable = computed(() => proto.roleSur(props.recrutementUuid) === 'responsable')

const activeTab = computed({
  get: () => props.tab,
  set: (tab) => {
    proto.page.value = { name: 'parametres-recrutement', recrutementUuid: props.recrutementUuid, tab }
  },
})

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements', to: '/recrutements' },
  { label: recrutement.value?.intitule ?? '', to: '/recrutements' },
  { label: 'Paramètres' },
])

const metaItems = computed<CspMetaItem[]>(() => recrutement.value
  ? [
      { icon: 'ri:briefcase-line', label: recrutement.value.intitule, srLabel: 'Offre' },
      { icon: 'ri:hashtag', label: recrutement.value.reference, srLabel: 'Référence' },
    ]
  : [])

const showSkeleton = useMinimumPending(proto.pending)

const columns = computed<CspColumnDef<MembreRow>[]>(() => [
  { id: 'membre', header: 'Membre', sortable: true, width: '14rem', accessor: row => formatAgentNomAlphabetique(row.agent), cellComponent: MembreCell },
  { id: 'role', header: 'Rôle sur l\'offre', sortable: true, width: '9rem', accessor: row => ROLE_OFFRE_LABELS[row.membre.roleOffre], cellComponent: RoleOffreCell },
  { id: 'fonction', header: 'Fonction', width: '9rem', accessor: row => row.membre.fonction },
  { id: 'email', header: 'Courriel', accessor: row => row.agent.email },
  { id: 'derniereActivite', header: 'Dernière activité', sortable: true, width: '9rem', wrapHeader: true, accessor: row => row.agent.dateDerniereActivite, cellComponent: ElapsedDaysCell },
  { id: 'dateCreation', header: 'Création de compte', width: '9rem', wrapHeader: true, accessor: row => shortDate.format(new Date(row.agent.dateCreation)) },
  ...(peutGerer.value ? [{ id: 'actions', header: '', align: 'end' as const, width: '3.5rem', cellComponent: MembreActionsCell }] : []),
])

const rows = computed<MembreRow[]>(() =>
  (recrutement.value?.membres ?? [])
    .map(membre => ({ membre, agent: proto.agentOf(membre.agentUuid), recrutementUuid: props.recrutementUuid }))
    .filter((row): row is MembreRow => row.agent !== null),
)

const { search, filtered } = useTextSearch(rows, row => [
  formatAgentNom(row.agent),
  formatAgentNomAlphabetique(row.agent),
  row.agent.email,
  row.membre.fonction,
])

const page = ref(1)

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'membre')} dans l'équipe`
})

const description = computed(() => {
  if (peutGerer.value)
    return 'L\'équipe regroupe les personnes qui participent au traitement des candidatures sur cette offre. Chaque ajout, retrait ou changement de rôle est tracé dans l\'activité de l\'offre.'
  return 'L\'équipe regroupe les personnes qui participent au traitement des candidatures sur cette offre. Seul un responsable de l\'offre peut la modifier.'
})

const ajoutOpen = ref(false)
const exclus = computed(() => rows.value.map(row => row.agent.uuid))

function handleAjout(resultat: AjoutMembreResultat): void {
  const agentUuid = resultat.type === 'agent'
    ? resultat.agentUuid
    : proto.inviterALaVolee(resultat.invitation, props.recrutementUuid).uuid
  proto.ajouterMembre(props.recrutementUuid, agentUuid, resultat.roleOffre, resultat.fonction)
  ajoutOpen.value = false
}

const retraitOpen = computed({
  get: () => retraitDemande.value?.recrutementUuid === props.recrutementUuid,
  set: (open) => {
    if (!open)
      annulerRetrait()
  },
})

function confirmerRetrait(): void {
  const demande = retraitDemande.value
  if (!demande)
    return
  proto.retirerMembre(demande.recrutementUuid, demande.agent.uuid)
  annulerRetrait()
}

const activites = computed(() => proto.activitesDe(props.recrutementUuid))
</script>

<template>
  <CspPageHeader
    title="Paramètres du recrutement"
    :breadcrumb="breadcrumb"
    :back-link="{ to: '/recrutements', label: 'Retour aux recrutements' }"
  >
    <template #subtitle>
      <CspMetaList :items="metaItems" />
    </template>
  </CspPageHeader>
  <CspPageContainer
    v-model:active-tab="activeTab"
    :tabs="TABS"
  >
    <template #tab-equipe>
      <section class="equipe-section">
        <div class="equipe-section__intro">
          <h2 class="equipe-section__title">
            Membres de l'équipe de recrutement
          </h2>
          <p class="equipe-section__description">
            {{ description }}
          </p>
        </div>

        <CspAsyncSection
          :pending="showSkeleton"
          loading-label="Chargement de l'équipe"
        >
          <template #skeleton>
            <CspSkeletonTable
              :rows="4"
              :columns="columns.length"
              with-footer
            />
          </template>

          <CspTableToolbar :count="countLabel">
            <CspInput
              v-model="search"
              type="search"
              aria-label="Rechercher une personne, un courriel"
              placeholder="Rechercher une personne, un courriel"
              class="equipe-section__search"
            />
            <CspButton
              v-if="peutGerer"
              label="Ajouter un membre"
              icon="ri:user-add-line"
              is-icon-left
              @click="ajoutOpen = true"
            />
          </CspTableToolbar>
          <CspDataTable
            v-model:page="page"
            :rows="filtered"
            :columns="columns"
            :row-key="row => row.agent.uuid"
            caption="Membres de l'équipe de recrutement"
            :page-size="PAGE_SIZE"
          >
            <template #empty>
              <CspEmptyState
                v-if="search"
                title="Aucun membre ne correspond à votre recherche."
                icon="ri:search-line"
              />
              <CspEmptyState
                v-else
                title="Cette offre n'a pas encore d'équipe."
                :description="peutGerer ? 'Ajoutez un responsable ou des recruteurs pour commencer à traiter les candidatures.' : 'Un gestionnaire de l\'organisme doit d\'abord désigner un responsable.'"
                icon="ri:team-line"
              >
                <template
                  v-if="peutGerer"
                  #action
                >
                  <CspButton
                    label="Ajouter un membre"
                    icon="ri:user-add-line"
                    is-icon-left
                    @click="ajoutOpen = true"
                  />
                </template>
              </CspEmptyState>
            </template>
          </CspDataTable>
        </CspAsyncSection>
      </section>
    </template>

    <template #tab-etapes>
      <CspEmptyState
        title="Étapes de recrutement de l'offre"
        description="Le paramétrage des étapes est celui de l'application actuelle et ne fait pas partie de ce prototype."
        icon="ri:list-ordered"
      />
    </template>

    <template #tab-activite>
      <section class="equipe-section">
        <div class="equipe-section__intro">
          <h2 class="equipe-section__title">
            Activité de l'offre
          </h2>
          <p class="equipe-section__description">
            Fil chronologique des changements d'équipe sur cette offre, du plus récent au plus ancien.
          </p>
        </div>
        <ActiviteList
          :evenements="activites"
          empty-title="Aucune activité sur cette offre."
        />
      </section>
    </template>
  </CspPageContainer>

  <AjoutMembreDrawer
    v-model:open="ajoutOpen"
    :recrutement-uuids="[recrutementUuid]"
    contexte="equipe"
    :exclus="exclus"
    :peut-inviter="estResponsable || proto.peutAssignerResponsables.value"
    @submit="handleAjout"
  />

  <ConfirmDialog
    v-model:open="retraitOpen"
    title="Retirer de l'équipe"
    confirm-label="Retirer"
    confirm-icon="ri:user-unfollow-line"
    @confirm="confirmerRetrait"
  >
    <template v-if="retraitDemande">
      {{ formatAgentNom(retraitDemande.agent) }} ne verra plus cette offre ni ses candidatures.
      Son compte reste actif dans l'organisme et il pourra être ajouté à nouveau.
    </template>
  </ConfirmDialog>
</template>

<style scoped lang="scss">
.equipe-section__intro {
  margin-bottom: var(--csp-space-5);
}

.equipe-section__title {
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
  font-weight: 600;
}

.equipe-section__description {
  margin: 0;
  max-width: 65ch;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.equipe-section__search {
  min-width: 20rem;
}
</style>
