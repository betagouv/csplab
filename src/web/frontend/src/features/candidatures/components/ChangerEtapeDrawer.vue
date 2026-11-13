<script setup lang="ts">
import type { EtapeRecrutement, KanbanColumn } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'
import { pluralize } from '@/utils/format'
import { etapeOptions, formatCandidatName } from '../format'

const props = defineProps<{
  open: boolean
  sourceEtape: KanbanColumn | null
  selectedCandidatureUuids: Set<string>
  etapes: EtapeRecrutement[]
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': [targetEtapeUuid: string]
  'toggleCandidature': [candidatureUuid: string, etapeUuid: string]
}>()

const selectedEtapeUuid = ref<string>('')

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    selectedEtapeUuid.value = ''
  }
})

const selectedCount = computed(() => props.selectedCandidatureUuids.size)
const selectedCountLabel = computed(() =>
  `${selectedCount.value} ${pluralize(selectedCount.value, 'candidature sélectionnée', 'candidatures sélectionnées')}`)

const options = computed(() => etapeOptions(props.etapes, props.sourceEtape?.uuid ?? ''))

const canConfirm = computed(() => {
  return selectedCount.value > 0 && selectedEtapeUuid.value !== '' && props.sourceEtape && selectedEtapeUuid.value !== props.sourceEtape.uuid
})

function handleConfirm(): void {
  if (canConfirm.value) {
    emit('confirm', selectedEtapeUuid.value)
  }
}

const selectedUuidsModel = computed({
  get: () => [...props.selectedCandidatureUuids],
  set: (uuids: string[]) => {
    if (!props.sourceEtape) {
      return
    }

    const prev = props.selectedCandidatureUuids
    const etapeUuid = props.sourceEtape.uuid

    for (const uuid of uuids) {
      if (!prev.has(uuid)) {
        emit('toggleCandidature', uuid, etapeUuid)
      }
    }

    for (const uuid of prev) {
      if (!uuids.includes(uuid)) {
        emit('toggleCandidature', uuid, etapeUuid)
      }
    }
  },
})
</script>

<template>
  <CspDrawer
    :open="open"
    size="md"
    :show-close="false"
    @update:open="emit('update:open', $event)"
  >
    <template #start>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:arrow-left-line"
        aria-label="Fermer"
        @click="emit('update:open', false)"
      />
    </template>

    <template #title>
      Changer d'étape
    </template>

    <div
      v-if="sourceEtape"
      class="changer-etape-drawer__content"
    >
      <section class="changer-etape-drawer__selection">
        <p class="changer-etape-drawer__count">
          {{ selectedCountLabel }}
        </p>

        <div class="changer-etape-drawer__tags">
          <CspTagGroup
            v-model="selectedUuidsModel"
            type="multiple"
            size="md"
          >
            <CspTag
              v-for="candidature in sourceEtape.candidatures"
              :key="candidature.uuid"
              :value="candidature.uuid"
              :label="formatCandidatName(candidature.candidat)"
              variant="selectable"
            />
          </CspTagGroup>
        </div>
      </section>

      <CspSeparator />

      <CspRadioGroup
        v-model="selectedEtapeUuid"
        label="Sélectionner l'étape où déplacer les candidatures"
        :options="options"
      />
    </div>

    <template #footer>
      <div class="changer-etape-drawer__footer">
        <CspButton
          label="Valider le changement d'étape"
          icon="ri:arrow-left-right-line"
          :disabled="!canConfirm"
          @click="handleConfirm"
        />
      </div>
    </template>
  </CspDrawer>
</template>

<style scoped lang="scss">
.changer-etape-drawer__content {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.changer-etape-drawer__selection {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.changer-etape-drawer__count {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.changer-etape-drawer__tags {
  max-height: 12rem;
  overflow-y: auto;
  padding-top: var(--csp-space-2);
}

.changer-etape-drawer__footer {
  width: 100%;

  :deep(.csp-btn) {
    width: 100%;
  }
}
</style>
