<script setup lang="ts">
import type { Persona } from '../data/mock'
import type { OrganismeTab, ProtoPage, RecrutementTab } from './useEquipePrototype'
import { computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import ParametresOrganismePage from '../pages/ParametresOrganismePage.vue'
import ParametresRecrutementPage from '../pages/ParametresRecrutementPage.vue'
import RecrutementsPage from '../pages/RecrutementsPage.vue'
import SansRecrutementPage from '../pages/SansRecrutementPage.vue'
import { provideEquipePrototype } from './context'
import PrototypeShell from './PrototypeShell.vue'
import { useEquipePrototype } from './useEquipePrototype'

export type InitialPage = 'recrutements' | 'equipe' | 'organisme'

const props = withDefaults(defineProps<{
  persona?: Persona
  initialPage?: InitialPage
}>(), {
  persona: 'gestionnaire',
  initialPage: 'recrutements',
})

const INITIAL_PAGES: Record<InitialPage, ProtoPage> = {
  recrutements: { name: 'recrutements' },
  equipe: { name: 'parametres-recrutement', recrutementUuid: 'rec-02', tab: 'equipe' },
  organisme: { name: 'parametres-organisme', tab: 'membres' },
}

const proto = useEquipePrototype(props.persona, INITIAL_PAGES[props.initialPage])
provideEquipePrototype(proto)

watch(() => props.persona, (value) => {
  proto.persona.value = value
})

const page = computed(() => proto.page.value)

const route = useRoute()
const router = useRouter()

function pathFor(target: ProtoPage): string {
  if (target.name === 'parametres-recrutement')
    return `/recrutements/${target.recrutementUuid}/parametres/${target.tab}`
  if (target.name === 'parametres-organisme')
    return `/organisme/parametres/${target.tab}`
  return '/recrutements'
}

function pageFor(path: string): ProtoPage | null {
  const recrutement = path.match(/^\/recrutements\/([\w-]+)\/parametres\/(equipe|etapes|activite)$/)
  if (recrutement)
    return { name: 'parametres-recrutement', recrutementUuid: recrutement[1], tab: recrutement[2] as RecrutementTab }
  const organisme = path.match(/^\/organisme\/parametres\/(membres|etapes|journal)$/)
  if (organisme)
    return { name: 'parametres-organisme', tab: organisme[1] as OrganismeTab }
  if (path === '/' || path === '/recrutements')
    return { name: 'recrutements' }
  return null
}

onMounted(() => {
  void router.replace(pathFor(proto.page.value))
})

watch(() => route.path, (path) => {
  const target = pageFor(path)
  if (target && pathFor(proto.page.value) !== path)
    proto.naviguer(target)
})

watch(proto.page, (target) => {
  const path = pathFor(target)
  if (route.path !== path)
    void router.replace(path)
})
</script>

<template>
  <CspToaster>
    <PrototypeShell>
      <SansRecrutementPage v-if="proto.sansRecrutement.value" />
      <ParametresRecrutementPage
        v-else-if="page.name === 'parametres-recrutement'"
        :key="page.recrutementUuid"
        :recrutement-uuid="page.recrutementUuid"
        :tab="page.tab"
      />
      <ParametresOrganismePage
        v-else-if="page.name === 'parametres-organisme'"
        :tab="page.tab"
      />
      <RecrutementsPage v-else />
    </PrototypeShell>
  </CspToaster>
</template>
