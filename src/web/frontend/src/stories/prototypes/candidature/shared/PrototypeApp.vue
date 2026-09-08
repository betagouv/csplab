<script setup lang="ts">
import type { InitialOpen } from './useCandidaturePrototype'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { pluralize } from '@/utils/format'
import { INTITULE_OFFRE } from '../data/mock'
import AccesRefuse from '../panel/AccesRefuse.vue'
import CandidaturePanel from '../panel/CandidaturePanel.vue'
import GardeFouDialog from '../panel/GardeFouDialog.vue'
import { provideCandidaturePrototype } from './context'
import PrototypeKanban from './PrototypeKanban.vue'
import PrototypeShell from './PrototypeShell.vue'
import { useCandidaturePrototype } from './useCandidaturePrototype'

const props = withDefaults(defineProps<{
  initialOpen?: InitialOpen
  accesRefuse?: boolean
}>(), {
  initialOpen: 'aucune',
  accesRefuse: false,
})

const proto = useCandidaturePrototype(props.initialOpen)
provideCandidaturePrototype(proto)

const breadcrumb: CspBreadcrumbItem[] = [
  { label: 'Accueil', to: '/' },
  { label: 'Recrutements', to: '/' },
  { label: INTITULE_OFFRE },
]

const TABS: CspTabItem<'candidatures' | 'activites'>[] = [
  { value: 'candidatures', label: 'Candidatures', icon: 'ri:group-line' },
  { value: 'activites', label: 'Activités et tâches', icon: 'ri:list-check' },
]
const activeTab = ref<'candidatures' | 'activites'>('candidatures')

const countLabel = computed(() => {
  const count = proto.scenario.etapes.reduce((sum, etape) => sum + etape.candidatureUuids.length, 0)
  return `${count} ${pluralize(count, 'candidature')}`
})
</script>

<template>
  <CspToastProvider>
    <PrototypeShell>
      <AccesRefuse v-if="accesRefuse" />
      <template v-else>
        <CspPageHeader
          :breadcrumb="breadcrumb"
          :title="INTITULE_OFFRE"
          :back-link="{ to: '/', label: 'Retour aux recrutements' }"
        />
        <CspPageContainer
          v-model:active-tab="activeTab"
          fill
          width="full"
          :tabs="TABS"
        >
          <template #tab-candidatures>
            <div class="proto-app__kanban">
              <p class="proto-app__count">
                {{ countLabel }}
              </p>
              <PrototypeKanban
                :etapes="proto.scenario.etapes"
                :candidature-of="proto.candidatureOf"
                :open-uuid="proto.candidature.value?.uuid ?? null"
                @open="proto.open($event)"
              />
            </div>
          </template>
          <template #tab-activites>
            <p class="proto-app__placeholder">
              Activités et tâches (à venir)
            </p>
          </template>
        </CspPageContainer>

        <CandidaturePanel />

        <GardeFouDialog
          :open="proto.pendingAction.value !== null"
          @continuer="proto.continueEditing()"
          @quitter="proto.quitWithoutSaving()"
        />
      </template>
    </PrototypeShell>

    <CspToast
      v-if="proto.etapeToast.value"
      :key="proto.etapeToast.value.candidatureUuid"
      open
      variant="success"
      title="Changement d'étape confirmé"
      :description="`${proto.etapeToast.value.candidatNom} est passé à l'étape « ${proto.etapeToast.value.etapeNom} ».`"
      :duration="10000"
      @update:open="(open) => { if (!open) proto.etapeToast.value = null }"
    >
      <CspButton
        label="Revenir à cette candidature"
        variant="tertiary-no-outline"
        size="sm"
        class="proto-app__toast-link"
        @click="proto.revenirCandidature()"
      />
    </CspToast>
    <CspToast
      v-if="proto.infoToast.value"
      :key="proto.infoToast.value.title"
      open
      variant="success"
      :title="proto.infoToast.value.title"
      :description="proto.infoToast.value.description ?? null"
      :duration="4000"
      @update:open="(open) => { if (!open) proto.infoToast.value = null }"
    />
  </CspToastProvider>
</template>

<style scoped lang="scss">
.proto-app__kanban {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.proto-app__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.proto-app__placeholder {
  color: var(--text-mention-grey);
}

.proto-app__toast-link {
  margin-top: var(--csp-space-1);
  margin-left: calc(var(--csp-space-2) * -1);
}
</style>
