<script setup lang="ts">
import { computed } from 'vue'
import { actionsRequises, documents } from '../../data/candidatMock'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = defineProps<{
  candidatureId: string
}>()

defineEmits<{
  retour: []
}>()

const documentsCandidature = computed(() => documents.filter(d => d.candidatureId === props.candidatureId))

function deposerDocument(docId: string) {
  const doc = documents.find(d => d.id === docId)
  if (!doc) {
    return
  }
  doc.statut = 'fourni'

  const index = actionsRequises.findIndex(a => a.candidatureId === doc.candidatureId && a.type === 'document')
  if (index !== -1) {
    actionsRequises.splice(index, 1)
  }
}
</script>

<template>
  <div class="documents">
    <MobileTopBar
      title="Documents"
      show-back
      @back="$emit('retour')"
    />

    <ul class="documents__list">
      <li
        v-for="doc in documentsCandidature"
        :key="doc.id"
        class="documents__item"
      >
        <CspIcon
          :name="doc.statut === 'fourni' ? 'ri:checkbox-circle-fill' : 'ri:error-warning-fill'"
          :size="20"
          class="documents__item-icon"
          :class="`documents__item-icon--${doc.statut}`"
        />
        <div class="documents__item-body">
          <p class="documents__item-nom">
            {{ doc.nom }}
          </p>
          <p class="documents__item-raison">
            {{ doc.raison }}
          </p>
          <CspButton
            v-if="doc.statut === 'a_fournir'"
            variant="primary"
            size="sm"
            label="Ajouter le document"
            class="documents__item-cta"
            @click="deposerDocument(doc.id)"
          />
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.documents {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.documents__list {
  list-style: none;
  margin: 0;
  padding: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.documents__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
}

.documents__item-icon {
  margin-top: 0.125rem;
  flex-shrink: 0;

  &--fourni {
    color: var(--text-default-success);
  }

  &--a_fournir {
    color: var(--text-default-warning);
  }
}

.documents__item-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.documents__item-nom {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.documents__item-raison {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.documents__item-cta {
  align-self: flex-start;
  margin-top: var(--csp-space-2);
}
</style>
