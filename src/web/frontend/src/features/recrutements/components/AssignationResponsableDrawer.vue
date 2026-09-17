<script setup lang="ts">
import type { RecrutementsActifs } from '../types'
import type { CspComboboxOption } from '@/components/base/CspCombobox/CspCombobox.vue'
import type { AgentOrganisme } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  recrutements: RecrutementsActifs[]
  agents: AgentOrganisme[]
  pendingAgents?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  remove: [offerId: string]
  assign: [agentId: string]
}>()

const open = defineModel<boolean>('open', { required: true })

const selectedAgentId = ref<string | null>(null)

const { search, filtered } = useTextSearch(() => props.agents, agent => [agent.email])

const options = computed<CspComboboxOption[]>(() => filtered.value.map(agent => ({
  value: agent.agent_id,
  label: agent.email,
})))

const offresLabel = computed(() => {
  const count = props.recrutements.length
  return `${count} ${pluralize(count, 'offre sélectionnée', 'offres sélectionnées')}`
})

const submitDisabled = computed(() => !selectedAgentId.value || props.submitting)

watch(open, (isOpen) => {
  if (!isOpen) {
    selectedAgentId.value = null
    search.value = ''
  }
})

watch(() => props.recrutements.length, (count) => {
  if (count === 0) {
    open.value = false
  }
})

function handleSubmit(): void {
  if (!selectedAgentId.value) {
    return
  }
  emit('assign', selectedAgentId.value)
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

      <CspCombobox
        v-model="selectedAgentId"
        v-model:search-term="search"
        :options="options"
        label="Responsable à assigner"
        hint="Seuls les membres de l'organisme peuvent être assignés."
        placeholder="Rechercher un courriel"
        name="agent"
        :pending="pendingAgents"
        empty-label="Aucun courriel disponible ne correspond à votre recherche"
      />

      <div class="assignation-responsable-drawer__actions">
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
        <CspButton
          type="submit"
          label="Assigner un responsable"
          icon="ri:user-star-line"
          is-icon-left
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
  margin: 0 0 var(--csp-space-3);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
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
