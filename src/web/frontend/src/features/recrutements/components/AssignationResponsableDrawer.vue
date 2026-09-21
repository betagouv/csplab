<script setup lang="ts">
import type { RecrutementsActifs } from '../types'
import type { AgentSearchStatus } from '@/features/organismes/composables/useAgentParEmail'
import type { AgentRecherche } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import AgentRechercheForm from '@/features/organismes/components/AgentRechercheForm.vue'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  recrutements: RecrutementsActifs[]
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  remove: [offerId: string]
  search: [email: string]
  assign: []
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })

const email = ref('')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() =>
  isFound.value ? 'Assigner un responsable' : 'Créer et assigner',
)

const offresLabel = computed(() => {
  const count = props.recrutements.length
  return `${count} ${pluralize(count, 'offre sélectionnée', 'offres sélectionnées')}`
})

watch(open, (isOpen) => {
  if (!isOpen) {
    email.value = ''
  }
})

watch(() => props.recrutements.length, (count) => {
  if (count === 0) {
    open.value = false
  }
})

function handleSubmit(): void {
  if (isSearched.value) {
    emit('assign')
  }
}
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Assigner un responsable"
    size="md"
  >
    <form
      class="assignation-responsable-drawer"
      novalidate
      @submit.prevent="handleSubmit"
    >
      <section>
        <p class="assignation-responsable-drawer__count">
          {{ offresLabel }}
        </p>
        <p class="assignation-responsable-drawer__lead">
          Le responsable sélectionné sera affecté à l'ensemble des offres sélectionnées.
        </p>
        <ul class="assignation-responsable-drawer__tags">
          <li
            v-for="recrutement in recrutements"
            :key="recrutement.offer_id"
          >
            <CspTag
              variant="dismissible"
              :label="recrutement.intitule"
              :dismiss-label="`Retirer ${recrutement.intitule} de la sélection`"
              @dismiss="emit('remove', recrutement.offer_id)"
            />
          </li>
        </ul>
      </section>

      <AgentRechercheForm
        v-model="email"
        label="Responsable"
        :status="status"
        :agent="agent"
        :searching="searching"
        @search="emit('search', $event)"
        @reset="emit('reset')"
      />

      <div class="assignation-responsable-drawer__actions">
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
        <CspButton
          v-if="isSearched"
          type="submit"
          :label="submitLabel"
          :disabled="submitting"
        />
      </div>
    </form>
  </CspDrawer>
</template>

<style scoped lang="scss">
.assignation-responsable-drawer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.assignation-responsable-drawer__count {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.assignation-responsable-drawer__lead {
  margin: var(--csp-space-1) 0 var(--csp-space-3);
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.assignation-responsable-drawer__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.assignation-responsable-drawer__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
