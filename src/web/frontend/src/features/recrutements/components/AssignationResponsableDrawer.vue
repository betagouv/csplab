<script setup lang="ts">
import type { ResponsableSearchStatus } from '../composables/useAssignationResponsable'
import type { RecrutementsActifs } from '../types'
import type { AgentRecherche } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { formatAgentName } from '@/features/organismes/format'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  recrutements: RecrutementsActifs[]
  status: ResponsableSearchStatus
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

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/

const email = ref('')
const error = ref('')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => {
  if (isFound.value) {
    return 'Assigner un responsable'
  }
  return isSearched.value ? 'Créer et assigner' : 'Rechercher'
})

const submitDisabled = computed(() => props.searching || props.submitting)

const offresLabel = computed(() => {
  const count = props.recrutements.length
  return `${count} ${pluralize(count, 'offre sélectionnée', 'offres sélectionnées')}`
})

watch(open, (isOpen) => {
  if (!isOpen) {
    email.value = ''
    error.value = ''
  }
})

watch(email, () => {
  error.value = ''
  if (props.status !== 'idle') {
    emit('reset')
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
    return
  }
  const value = email.value.trim()
  if (!EMAIL_PATTERN.test(value)) {
    error.value = 'Renseignez une adresse électronique valide.'
    return
  }
  error.value = ''
  emit('search', value)
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

      <CspInput
        v-model="email"
        label="Responsable"
        name="email"
        type="email"
        placeholder="prenom.nom@exemple.gouv.fr"
        autocomplete="off"
        :error="Boolean(error)"
        :error-message="error"
      />

      <div
        v-if="isFound && agent"
        class="assignation-responsable-drawer__agent"
      >
        <p class="assignation-responsable-drawer__agent-name">
          {{ formatAgentName(agent) || agent.email }}
        </p>
        <p class="assignation-responsable-drawer__agent-detail">
          {{ agent.intitule_poste }}
        </p>
        <p class="assignation-responsable-drawer__agent-detail">
          {{ agent.email }}
        </p>
      </div>

      <p
        v-else-if="status === 'not-found'"
        class="assignation-responsable-drawer__hint"
      >
        Aucun compte ne correspond à cette adresse. Un compte sera créé, la personne
        complétera son profil à sa première connexion.
      </p>

      <div class="assignation-responsable-drawer__actions">
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
        <CspButton
          type="submit"
          :label="submitLabel"
          :disabled="submitDisabled"
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

.assignation-responsable-drawer__hint {
  margin: 0;
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

.assignation-responsable-drawer__agent {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.25rem;
}

.assignation-responsable-drawer__agent-name {
  margin: 0;
  font-weight: 600;
}

.assignation-responsable-drawer__agent-detail {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.assignation-responsable-drawer__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
