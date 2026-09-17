<script setup lang="ts">
import { computed } from 'vue'
import { actionsRequises, candidatureParId, documents } from '../../data/candidatMock'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = defineProps<{
  initialCandidatureId?: string | null
}>()

const groupes = computed(() => {
  const parCandidature = new Map<string, typeof documents>()
  for (const doc of documents) {
    const liste = parCandidature.get(doc.candidatureId) ?? []
    liste.push(doc)
    parCandidature.set(doc.candidatureId, liste)
  }
  return [...parCandidature.entries()].map(([candidatureId, docs]) => ({
    candidature: candidatureParId(candidatureId),
    docs,
    aUneDemande: docs.some(d => d.statut === 'a_fournir'),
  }))
})

function estOuvertParDefaut(candidatureId: string | undefined, aUneDemande: boolean) {
  return candidatureId === props.initialCandidatureId || aUneDemande
}

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
    <MobileTopBar title="Documents" />

    <div class="documents__content">
      <details
        v-for="groupe in groupes"
        :key="groupe.candidature?.id"
        class="documents__groupe"
        :open="estOuvertParDefaut(groupe.candidature?.id, groupe.aUneDemande)"
      >
        <summary>
          <span class="documents__groupe-titre">
            {{ groupe.candidature?.poste }}
          </span>
          <CspBadge
            v-if="groupe.aUneDemande"
            label="À fournir"
            type="warning"
            size="sm"
          />
          <CspIcon
            name="ri:arrow-down-s-line"
            :size="18"
            class="documents__groupe-icon"
          />
        </summary>

        <ul class="documents__list">
          <li
            v-for="doc in groupe.docs"
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
            </div>
          </li>
        </ul>

        <CspButton
          v-if="groupe.aUneDemande"
          variant="primary"
          size="md"
          label="Ajouter le document"
          class="documents__ajouter"
          @click="deposerDocument(groupe.docs.find(d => d.statut === 'a_fournir')!.id)"
        />
      </details>
    </div>
  </div>
</template>

<style scoped lang="scss">
.documents {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.documents__content {
  padding: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.documents__groupe {
  padding: var(--csp-space-3);
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);

  summary {
    display: flex;
    align-items: center;
    gap: var(--csp-space-2);
    cursor: pointer;
    list-style: none;
    min-height: 2rem;

    &::-webkit-details-marker {
      display: none;
    }
  }

  &[open] summary .documents__groupe-icon {
    transform: rotate(180deg);
  }
}

.documents__groupe-titre {
  flex: 1;
  min-width: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.documents__groupe-icon {
  flex-shrink: 0;
  transition: transform 0.15s ease;
  color: var(--text-mention-grey);
}

.documents__list {
  list-style: none;
  margin: var(--csp-space-3) 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.documents__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
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
}

.documents__item-nom {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.documents__item-raison {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.documents__ajouter {
  width: 100%;
  justify-content: center;
  margin-top: var(--csp-space-3);
}
</style>
