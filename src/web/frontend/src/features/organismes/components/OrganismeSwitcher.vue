<script setup lang="ts">
import type { CspSidebarSwitcherGroup } from '@/components/layout/CspSidebar/CspSidebarSwitcher.vue'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspSidebarSwitcher from '@/components/layout/CspSidebar/CspSidebarSwitcher.vue'
import { organismeHomeLocation, ORGANISMES_ROUTE_NAME } from '@/router/names'
import { useCurrentUser } from '@/stores/currentUser'
import { organismeDetailQuery } from '@/stores/organismeDetail'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { can } from '@/utils/authorizedActions'
import { useOrganismesSearch } from '../composables/useOrganismesSearch'
import { ESPACE_ADMINISTRATEUR_LABEL, ORGANISME_LABEL } from '../constants/organisme'

const ESPACE_ADMINISTRATEUR = 'espace-administrateur'

const router = useRouter()
const { user } = useCurrentUser()
const { organismes, organisme, organismeUuid } = useRouteOrganisme()
const { search, results, tooShort, searching } = useOrganismesSearch()

const canBrowseOrganismes = computed(() => can(user.value?.authorized_actions, 'list_organismes'))

const { data: organismeHorsAppartenance } = useQuery(() => ({
  ...organismeDetailQuery({ organismeUuid: organismeUuid.value ?? '' }),
  enabled: canBrowseOrganismes.value && Boolean(organismeUuid.value) && !organisme.value,
}))

const title = computed(() => {
  if (!canBrowseOrganismes.value) {
    return organisme.value?.nom ?? null
  }
  if (!organismeUuid.value) {
    return ESPACE_ADMINISTRATEUR_LABEL
  }
  return organisme.value?.nom
    ?? organismeHorsAppartenance.value?.nom
    ?? ORGANISME_LABEL
})

const ariaLabel = computed(() => canBrowseOrganismes.value
  ? `${title.value}. Changer d'espace`
  : `Organisme : ${title.value}. Changer d'organisme`)

const emptyLabel = computed(() => {
  if (tooShort.value) {
    return 'Saisissez au moins 3 caractères'
  }
  return searching.value ? 'Recherche en cours…' : 'Aucun organisme trouvé'
})

const memberOptions = computed(() => organismes.value.map(member => ({
  value: member.uuid,
  label: member.nom,
})))

const groups = computed<CspSidebarSwitcherGroup[]>(() => {
  if (!canBrowseOrganismes.value) {
    return [{ label: 'Changer d\'organisme', options: memberOptions.value }]
  }
  if (search.value.trim()) {
    return [{
      options: results.value.map(listed => ({
        value: listed.uuid,
        label: listed.nom,
        description: listed.siret,
      })),
    }]
  }
  return [
    { options: [{ value: ESPACE_ADMINISTRATEUR, label: ESPACE_ADMINISTRATEUR_LABEL }] },
    { label: 'Membre de', options: memberOptions.value },
  ]
})

function select(value: string) {
  if (value === ESPACE_ADMINISTRATEUR) {
    void router.push({ name: ORGANISMES_ROUTE_NAME })
    return
  }
  if (value === organismeUuid.value) {
    return
  }
  void router.push(organismeHomeLocation(value))
}
</script>

<template>
  <CspSidebarSwitcher
    v-if="title"
    v-model:search="search"
    :title="title"
    :groups="groups"
    :selected="organismeUuid ?? ESPACE_ADMINISTRATEUR"
    :filter-label="canBrowseOrganismes ? 'Accéder à un organisme' : undefined"
    filter-placeholder="Nom de l'organisme"
    :empty-label="emptyLabel"
    :aria-label="ariaLabel"
    @select="select"
  >
    <template #leading>
      <CspAvatar
        :icon="organismeUuid ? 'ri:government-fill' : 'ri:shield-user-fill'"
      />
    </template>
  </CspSidebarSwitcher>
</template>
