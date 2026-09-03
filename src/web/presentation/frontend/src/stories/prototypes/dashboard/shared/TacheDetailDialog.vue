<script setup lang="ts">
import type { TacheDashboard } from '../data/dashboardMock'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

const props = defineProps<{
  open: boolean
  tache: TacheDashboard | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'toggleFait': [id: string]
  'voirRecrutement': [id: string]
}>()

function toggleFait() {
  if (props.tache)
    emit('toggleFait', props.tache.id)
}

function voirRecrutement() {
  if (props.tache?.recrutementId)
    emit('voirRecrutement', props.tache.recrutementId)
}
</script>

<template>
  <CspDialog
    :open="open"
    size="md"
    :title="tache?.libelle"
    @update:open="value => emit('update:open', value)"
  >
    <template v-if="tache">
      <dl class="tache-dialog__fields">
        <div
          v-if="tache.recrutementIntitule"
          class="tache-dialog__field"
        >
          <dt>Recrutement concerné</dt>
          <dd>{{ tache.recrutementIntitule }}</dd>
        </div>
        <div
          v-if="tache.candidatNom"
          class="tache-dialog__field"
        >
          <dt>Candidature concernée</dt>
          <dd>{{ tache.candidatNom }}</dd>
        </div>
        <div class="tache-dialog__field">
          <dt>Échéance</dt>
          <dd>
            <CspBadge
              :type="tache.echeanceStatut === 'retard' ? 'error' : tache.echeanceStatut === 'aujourdhui' ? 'warning' : undefined"
              :label="tache.echeanceLabel"
            />
          </dd>
        </div>
        <div class="tache-dialog__field">
          <dt>Assignée à</dt>
          <dd class="tache-dialog__assignee">
            <CspAvatar
              :name="tache.assigneA"
              size="sm"
            />
            {{ tache.assigneA }}
          </dd>
        </div>
      </dl>
    </template>

    <template #footer>
      <CspButton
        v-if="tache?.recrutementId"
        variant="tertiary"
        label="Voir le recrutement"
        @click="voirRecrutement"
      />
      <CspButton
        :variant="tache?.fait ? 'secondary' : 'primary'"
        :label="tache?.fait ? 'Marquer à faire' : 'Marquer comme faite'"
        :icon="tache?.fait ? undefined : 'ri:checkbox-circle-line'"
        @click="toggleFait"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.tache-dialog__fields {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
  margin: 0;
}

.tache-dialog__field {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;

  dt {
    font-size: 0.875rem;
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-title-grey);
  }
}

.tache-dialog__assignee {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
