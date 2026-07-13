<script setup lang="ts">
import type { Candidature, EtapeRecrutementDetailedCandidatures } from '../types'
import { computed, ref, watch } from 'vue'
import { RadioGroupIndicator, RadioGroupItem, RadioGroupRoot } from 'reka-ui'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'

const props = defineProps<{
  open: boolean
  sourceEtape: EtapeRecrutementDetailedCandidatures | null
  selectedCandidatureUuids: Set<string>
  etapes: EtapeRecrutementDetailedCandidatures[]
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': [targetEtapeUuid: string]
  'toggle-candidature': [candidatureUuid: string, etapeUuid: string]
}>()

const selectedEtapeUuid = ref<string>('')

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    selectedEtapeUuid.value = ''
  }
})

const selectedCount = computed(() => props.selectedCandidatureUuids.size)

const canConfirm = computed(() => {
  return selectedCount.value > 0 && selectedEtapeUuid.value !== '' && props.sourceEtape && selectedEtapeUuid.value !== props.sourceEtape.etape_uuid
})

function handleConfirm(): void {
  if (canConfirm.value) {
    emit('confirm', selectedEtapeUuid.value)
  }
}

function getCandidatName(candidature: Candidature): string {
  const candidat = candidature.candidat
  return `${candidat.prenom} ${candidat.nom}`
}

const selectedUuidsModel = computed({
  get: () => [...props.selectedCandidatureUuids],
  set: (uuids: string[]) => {
    if (!props.sourceEtape)
      return

    const prev = props.selectedCandidatureUuids
    const etapeUuid = props.sourceEtape.etape_uuid

    for (const uuid of uuids) {
      if (!prev.has(uuid)) {
        emit('toggle-candidature', uuid, etapeUuid)
      }
    }

    for (const uuid of prev) {
      if (!uuids.includes(uuid)) {
        emit('toggle-candidature', uuid, etapeUuid)
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
    <template #title>
      <div class="changer-etape-drawer__title-row">
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:arrow-left-line"
          aria-label="Fermer"
          @click="emit('update:open', false)"
        />
        <span>Changer d'étape</span>
      </div>
    </template>

    <div
      v-if="sourceEtape"
      class="changer-etape-drawer__content"
    >
      <section class="changer-etape-drawer__selection">
        <p class="changer-etape-drawer__count">
          {{ selectedCount }} candidature{{ selectedCount > 1 ? 's' : '' }} sélectionnée{{ selectedCount > 1 ? 's' : '' }}
        </p>

        <CspTagGroup
          v-model="selectedUuidsModel"
          type="multiple"
          size="md"
        >
          <CspTag
            v-for="candidature in sourceEtape.candidatures"
            :key="candidature.uuid"
            :value="candidature.uuid"
            :label="getCandidatName(candidature)"
            variant="selectable"
          />
        </CspTagGroup>
      </section>

      <section class="changer-etape-drawer__etapes">
        <p class="changer-etape-drawer__etapes-label">
          Sélectionner l'étape où déplacer les candidatures
        </p>

        <RadioGroupRoot
          v-model="selectedEtapeUuid"
          class="changer-etape-drawer__radio-group"
          orientation="vertical"
        >
          <label
            v-for="etape in etapes"
            :key="etape.etape_uuid"
            class="changer-etape-drawer__radio"
            :class="{
              'changer-etape-drawer__radio--current': etape.etape_uuid === sourceEtape.etape_uuid,
            }"
          >
            <RadioGroupItem
              class="changer-etape-drawer__radio-control"
              :value="etape.etape_uuid"
              :disabled="etape.etape_uuid === sourceEtape.etape_uuid"
            >
              <RadioGroupIndicator class="changer-etape-drawer__radio-indicator" />
            </RadioGroupItem>
            <span class="changer-etape-drawer__radio-content">
              <span class="changer-etape-drawer__radio-label">{{ etape.nom }}</span>
              <span
                v-if="etape.etape_uuid === sourceEtape.etape_uuid"
                class="changer-etape-drawer__radio-hint"
              >
                Étape actuelle
              </span>
            </span>
          </label>
        </RadioGroupRoot>
      </section>
    </div>

    <template #footer>
      <CspButton
        label="Valider le changement d'étape"
        icon="ri:arrow-left-right-line"
        :disabled="!canConfirm"
        @click="handleConfirm"
      />
    </template>
  </CspDrawer>
</template>

<style scoped lang="scss">
.changer-etape-drawer__title-row {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.changer-etape-drawer__content {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.changer-etape-drawer__selection {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.changer-etape-drawer__count {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.changer-etape-drawer__etapes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.changer-etape-drawer__etapes-label {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-default-grey);
}

.changer-etape-drawer__radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.changer-etape-drawer__radio {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  cursor: pointer;
}

.changer-etape-drawer__radio--current {
  cursor: not-allowed;

  .changer-etape-drawer__radio-label {
    color: var(--text-mention-grey);
  }
}

.changer-etape-drawer__radio-control {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  flex: 0 0 auto;
  margin-top: 0.0625rem;
  border-radius: 50%;
  border: 1px solid var(--border-default-grey);
  background: transparent;
  padding: 0;
  cursor: inherit;

  &[data-state='checked'] {
    border-color: var(--background-action-high-blue-france);
  }

  &[data-disabled] {
    border-color: var(--border-disabled-grey);
    background: var(--background-disabled-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.changer-etape-drawer__radio-indicator {
  display: block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--background-action-high-blue-france);
}

.changer-etape-drawer__radio-content {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.changer-etape-drawer__radio-label {
  font-size: 0.9375rem;
  line-height: 1.3;
  color: var(--text-default-grey);
}

.changer-etape-drawer__radio-hint {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
