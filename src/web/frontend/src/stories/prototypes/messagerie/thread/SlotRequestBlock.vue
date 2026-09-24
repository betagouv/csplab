<script setup lang="ts">
import type { SlotRequest } from '../shared/types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { formatAbsolute, formatSlot } from '../shared/format'

const props = defineProps<{
  request: SlotRequest
  viewer: 'candidat' | 'recruteur'
  candidateName: string
}>()

const emit = defineEmits<{
  choose: [slotId: string]
}>()

const titleId = useId()
const selected = ref('')

const options = computed(() =>
  props.request.slots.map(slot => ({ value: slot.id, label: formatSlot(slot.start) })),
)

const chosen = computed(() =>
  props.request.slots.find(slot => slot.id === props.request.chosenSlotId),
)

const deadline = computed(() => formatSlot(props.request.deadline))
</script>

<template>
  <section
    class="slot-request"
    :aria-labelledby="titleId"
  >
    <template v-if="chosen">
      <h4
        :id="titleId"
        class="slot-request__title"
      >
        <CspIcon
          name="ri:calendar-check-line"
          :size="20"
          class="slot-request__icon"
        />
        Créneau retenu : {{ formatSlot(chosen.start) }}
      </h4>
      <p
        v-if="request.chosenAt"
        class="slot-request__meta"
      >
        <template v-if="viewer === 'candidat'">
          Vous avez choisi ce créneau le {{ formatAbsolute(request.chosenAt) }}. L’équipe de recrutement en est informée.
        </template>
        <template v-else>
          Choisi par {{ candidateName }} le {{ formatAbsolute(request.chosenAt) }}.
        </template>
      </p>
    </template>

    <template v-else-if="viewer === 'candidat'">
      <h4
        :id="titleId"
        class="slot-request__title"
      >
        Choisissez un créneau d’entretien
      </h4>
      <p class="slot-request__meta">
        Réponse attendue avant le {{ deadline }}.
      </p>
      <CspRadioGroup
        v-model="selected"
        :options="options"
        name="creneau"
        label="Créneaux proposés"
        class="slot-request__options"
      />
      <div class="slot-request__actions">
        <CspButton
          label="Confirmer ce créneau"
          :disabled="!selected"
          @click="emit('choose', selected)"
        />
      </div>
      <p class="slot-request__meta">
        Si aucun créneau ne vous convient, répondez à ce message.
      </p>
    </template>

    <template v-else>
      <h4
        :id="titleId"
        class="slot-request__title"
      >
        Créneaux proposés
      </h4>
      <ul class="slot-request__list">
        <li
          v-for="option in options"
          :key="option.value"
        >
          {{ option.label }}
        </li>
      </ul>
      <p class="slot-request__meta">
        En attente du choix de {{ candidateName }}, avant le {{ deadline }}.
      </p>
    </template>
  </section>
</template>

<style scoped>
.slot-request {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  max-width: 34rem;
  padding: var(--csp-space-4);
  background: var(--background-alt-blue-france);
}

.slot-request__title {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.slot-request__icon {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}

.slot-request__meta {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.slot-request__list {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-base);
  list-style: disc;
}

.slot-request__actions {
  display: flex;
}
</style>
