<script setup lang="ts">
import type { RecrutementsActifs } from '../types'
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  recrutements: RecrutementsActifs[]
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  remove: [recrutementUuid: string]
  search: [email: string]
  assign: []
  reset: []
  cancel: []
}>()

const email = ref('')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() =>
  props.status === 'not-found' ? 'Créer et assigner' : 'Assigner un responsable',
)

const recrutementsLabel = computed(() => {
  const count = props.recrutements.length
  return `${count} ${pluralize(count, 'recrutement sélectionné', 'recrutements sélectionnés')}`
})

function handleSubmit(): void {
  if (isSearched.value) {
    emit('assign')
  }
}
</script>

<template>
  <form
    class="assign-responsable-form"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <section>
      <p class="assign-responsable-form__count">
        {{ recrutementsLabel }}
      </p>
      <p class="assign-responsable-form__lead">
        Le responsable sélectionné sera affecté à l'ensemble des recrutements sélectionnés.
      </p>
      <ul class="assign-responsable-form__tags">
        <li
          v-for="recrutement in recrutements"
          :key="recrutement.uuid"
        >
          <CspTag
            variant="dismissible"
            :label="recrutement.intitule"
            :dismiss-label="`Retirer ${recrutement.intitule} de la sélection`"
            @dismiss="emit('remove', recrutement.uuid)"
          />
        </li>
      </ul>
    </section>

    <AgentRechercheForm
      v-model="email"
      label="Responsable"
      hint="Saisissez le courriel de l'agent."
      :status="status"
      :agent="agent"
      :searching="searching"
      @search="emit('search', $event)"
      @reset="emit('reset')"
    />

    <div class="assign-responsable-form__actions">
      <CspButton
        variant="secondary"
        type="button"
        label="Annuler"
        @click="emit('cancel')"
      />
      <CspButton
        type="submit"
        :label="submitLabel"
        :disabled="!isSearched || submitting"
      />
    </div>
  </form>
</template>

<style scoped lang="scss">
.assign-responsable-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.assign-responsable-form__count {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.assign-responsable-form__lead {
  margin: var(--csp-space-1) 0 var(--csp-space-3);
  color: var(--text-mention-grey);
  font-size: var(--csp-font-size-xs);
}

.assign-responsable-form__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.assign-responsable-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
