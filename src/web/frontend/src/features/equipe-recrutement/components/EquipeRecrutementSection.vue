<script setup lang="ts">
import type { AjoutMembrePayload } from '../types'
import { computed, ref, watch } from 'vue'
import { HttpError } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useToast } from '@/composables/ui/useToast'
import { formatAgentName } from '@/features/organismes/format'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { pluralize } from '@/utils/format'
import { EQUIPE_RECRUTEMENT_COLUMNS } from '../columns'
import { useAjoutMembreEquipe } from '../composables/useAjoutMembreEquipe'
import { useEquipeRecrutement } from '../composables/useEquipeRecrutement'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const PAGE_SIZE = 8

const { membres, pending, error } = useEquipeRecrutement(props.organismeUuid, props.recrutementUuid)
const { agentsDisponibles, pendingAgents, add, submitting } = useAjoutMembreEquipe(
  props.organismeUuid,
  props.recrutementUuid,
)
const { canManageOrganisme } = useRouteOrganisme()
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const page = ref(1)
const ajoutDrawerOpen = ref(false)

function ajoutErrorTitle(submitError: unknown): string {
  if (submitError instanceof HttpError && submitError.status === 409)
    return 'Cet agent fait déjà partie de l\'équipe'
  if (submitError instanceof HttpError && submitError.status === 404)
    return 'Cet agent n\'est plus rattaché à l\'organisme'
  return 'L\'ajout du membre a échoué'
}

async function handleAdd(payload: AjoutMembrePayload) {
  try {
    const membre = await add(payload)
    addToast({
      variant: 'success',
      title: 'Membre ajouté',
      description: `${formatAgentName(membre)} a rejoint l'équipe de recrutement.`,
    })
    ajoutDrawerOpen.value = false
  }
  catch (submitError) {
    addToast({ variant: 'error', title: ajoutErrorTitle(submitError) })
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
          :columns="EQUIPE_RECRUTEMENT_COLUMNS.length"
          with-footer
        />
      </template>

      <CspTableToolbar :count="countLabel">
        <CspInput
          v-model="search"
          type="search"
          aria-label="Rechercher un membre, un courriel"
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
        :columns="EQUIPE_RECRUTEMENT_COLUMNS"
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
      v-model:open="ajoutDrawerOpen"
      :agents="agentsDisponibles"
      :pending-agents="pendingAgents"
      :submitting="submitting"
      @add="handleAdd"
    />
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
</style>
