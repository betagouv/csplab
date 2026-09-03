<script setup lang="ts">
import type { RecrutementDashboard } from '../data/dashboardMock'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'

const props = defineProps<{
  open: boolean
  recrutement: RecrutementDashboard | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'voirCandidatures': [id: string]
}>()

const metaItems = computed(() => {
  if (!props.recrutement)
    return []
  return [
    { icon: 'ri:hashtag', srLabel: 'Référence RenoiRH', label: `Réf. RenoiRH ${props.recrutement.referenceRenoiRH}` },
    { icon: 'ri:building-line', srLabel: 'Service', label: props.recrutement.service },
    { icon: 'ri:file-list-3-line', srLabel: 'Type de contrat', label: props.recrutement.typeContrat },
  ]
})

function voirCandidatures() {
  if (props.recrutement)
    emit('voirCandidatures', props.recrutement.id)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="md"
    :title="recrutement?.intitule"
    @update:open="value => emit('update:open', value)"
  >
    <template v-if="recrutement">
      <CspMetaList
        :items="metaItems"
        size="md"
      />

      <p class="recrutement-dialog__date">
        {{ recrutement.datePublicationLabel }}
      </p>

      <dl class="recrutement-dialog__stats">
        <div class="recrutement-dialog__stat">
          <dt>Nouveaux CV</dt>
          <dd>
            <CspBadge
              v-if="recrutement.nouveauxCV > 0"
              type="new"
              :label="String(recrutement.nouveauxCV)"
            />
            <span v-else>0</span>
          </dd>
        </div>
        <div class="recrutement-dialog__stat">
          <dt>Candidatures au total</dt>
          <dd>{{ recrutement.candidaturesTotal }}</dd>
        </div>
        <div class="recrutement-dialog__stat">
          <dt>Candidatures en attente</dt>
          <dd>{{ recrutement.candidaturesEnAttente }}</dd>
        </div>
        <div class="recrutement-dialog__stat">
          <dt>Entretiens à préparer</dt>
          <dd>{{ recrutement.entretiensAPreparer }}</dd>
        </div>
      </dl>
    </template>

    <template #footer>
      <CspButton
        variant="secondary"
        label="Fermer"
        @click="emit('update:open', false)"
      />
      <CspButton
        variant="primary"
        label="Voir les candidatures"
        icon="ri:arrow-right-line"
        @click="voirCandidatures"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.recrutement-dialog__date {
  margin: -0.5rem 0 1rem;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.recrutement-dialog__stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 0;
  padding-top: 1rem;
  border-top: 1px solid var(--border-default-grey);
}

.recrutement-dialog__stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;

  dt {
    font-size: 0.75rem;
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-title-grey);
  }
}
</style>
