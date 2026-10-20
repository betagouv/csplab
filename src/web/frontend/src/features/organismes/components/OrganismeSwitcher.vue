<script setup lang="ts">
import type { CspSidebarSwitcherGroup } from '@/components/layout/CspSidebar/CspSidebarSwitcher.vue'
import { useQuery } from '@pinia/colada'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspSidebarSwitcher from '@/components/layout/CspSidebar/CspSidebarSwitcher.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { ORGANISMES_ROUTE_NAME, RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'
import { useCurrentUser } from '@/stores/currentUser'
import { useRouteOrganisme } from '@/stores/routeOrganisme'
import { ESPACE_ADMINISTRATEUR_LABEL, ORGANISME_LABEL } from '../constants/organisme'
import { organismesListQuery } from '../queries'

const ESPACE_ADMINISTRATEUR = 'espace-administrateur'

const router = useRouter()
const { isStaff } = useCurrentUser()
const { organismes, organisme, organismeUuid } = useRouteOrganisme()

const { data: allOrganismes } = useQuery(() => ({
  ...organismesListQuery,
  enabled: isStaff.value,
}))

const { search, filtered } = useTextSearch(
  () => allOrganismes.value ?? [],
  listed => [listed.nom, listed.siret],
  0,
)

const title = computed(() => {
  if (!isStaff.value) {
    return organisme.value?.nom ?? null
  }
  if (!organismeUuid.value) {
    return ESPACE_ADMINISTRATEUR_LABEL
  }
  return organisme.value?.nom
    ?? allOrganismes.value?.find(listed => listed.uuid === organismeUuid.value)?.nom
    ?? ORGANISME_LABEL
})

const ariaLabel = computed(() => isStaff.value
  ? `${title.value}. Changer d'espace`
  : `Organisme : ${title.value}. Changer d'organisme`)

const memberOptions = computed(() => organismes.value.map(role => ({
  value: role.organisme_uuid,
  label: role.nom,
})))

const groups = computed<CspSidebarSwitcherGroup[]>(() => {
  if (!isStaff.value) {
    return [{ label: 'Changer d\'organisme', options: memberOptions.value }]
  }
  if (search.value.trim()) {
    return [{
      options: filtered.value.map(listed => ({
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
  void router.push({
    name: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs,
    params: { organismeUuid: value },
  })
}
</script>

<template>
  <CspSidebarSwitcher
    v-if="title"
    v-model:search="search"
    :title="title"
    :groups="groups"
    :selected="organismeUuid ?? ESPACE_ADMINISTRATEUR"
    :filter-label="isStaff ? 'Accéder à un organisme' : undefined"
    filter-placeholder="Nom ou SIRET"
    empty-label="Aucun organisme trouvé"
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
