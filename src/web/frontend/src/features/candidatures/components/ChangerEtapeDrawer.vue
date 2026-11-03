<script setup lang="ts">
import type { EtapeRecrutement, EtapeRecrutementDetailedCandidatures } from '../types'
import { RadioGroupIndicator, RadioGroupItem, RadioGroupRoot } from 'reka-ui'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspSelectionSummary from '@/components/base/CspSelectionSummary/CspSelectionSummary.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  open: boolean
  sourceEtape: EtapeRecrutementDetailedCandidatures | null
  selectedCount: number
  etapes: EtapeRecrutement[]
  initialEtapeUuid?: string | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirm': [targetEtapeUuid: string]
}>()

const selectedEtapeUuid = ref<string>('')

watch(() => props.open, (isOpen) => {
  if (isOpen) {
    selectedEtapeUuid.value = props.initialEtapeUuid ?? ''
  }
})

const candidaturesLabel = computed(() =>
  `${props.selectedCount} ${pluralize(props.selectedCount, 'candidature')}`)

const summary = computed(() => `${candidaturesLabel.value} de la colonne ${props.sourceEtape?.nom}`)

const canConfirm = computed(() => {
  return props.selectedCount > 0 && selectedEtapeUuid.value !== '' && props.sourceEtape && selectedEtapeUuid.value !== props.sourceEtape.uuid
})

function handleConfirm(): void {
  if (canConfirm.value) {
    emit('confirm', selectedEtapeUuid.value)
  }
}
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
      <CspSelectionSummary
        :summary="summary"
        @edit="emit('update:open', false)"
      />

      <CspSeparator />

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
            :key="etape.uuid"
            class="changer-etape-drawer__radio"
            :class="{
              'changer-etape-drawer__radio--current': etape.uuid === sourceEtape.uuid,
            }"
          >
            <RadioGroupItem
              class="changer-etape-drawer__radio-control"
              :value="etape.uuid"
              :disabled="etape.uuid === sourceEtape.uuid"
            >
              <RadioGroupIndicator class="changer-etape-drawer__radio-indicator" />
            </RadioGroupItem>
            <span class="changer-etape-drawer__radio-content">
              <span class="changer-etape-drawer__radio-label">{{ etape.nom }}</span>
              <span
                v-if="etape.uuid === sourceEtape.uuid"
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
      <div class="changer-etape-drawer__footer">
        <CspButton
          :label="`Déplacer ${candidaturesLabel}`"
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

.changer-etape-drawer__footer {
  width: 100%;

  :deep(.csp-btn) {
    width: 100%;
  }
}

.changer-etape-drawer__etapes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.changer-etape-drawer__etapes-label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: 600;
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
  border: 1px solid var(--border-action-high-blue-france);
  background: transparent;
  padding: 0;
  cursor: inherit;

  &[data-state='checked'] {
    border-color: var(--border-active-blue-france);
  }

  &[data-disabled] {
    border-color: var(--border-disabled-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.changer-etape-drawer__radio:not(.changer-etape-drawer__radio--current) {
  &:hover .changer-etape-drawer__radio-control {
    background: var(--background-default-grey-hover);
  }

  &:active .changer-etape-drawer__radio-control {
    background: var(--background-default-grey-active);
  }
}

.changer-etape-drawer__radio-indicator {
  display: block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--background-active-blue-france);

  &[data-disabled] {
    background: var(--background-disabled-grey);
  }
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
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
