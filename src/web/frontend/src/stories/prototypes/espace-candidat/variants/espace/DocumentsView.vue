<script setup lang="ts">
import { computed, ref } from 'vue'
import { actionsRequises, candidatureParId, documents } from '../../data/candidatMock'
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
  }))
})

const enSurbrillance = ref(props.initialCandidatureId ?? null)

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
    <h1 class="documents__title">
      Documents
    </h1>

    <div
      v-for="groupe in groupes"
      :key="groupe.candidature?.id"
      class="documents__groupe"
      :class="{ 'documents__groupe--surligne': groupe.candidature?.id === enSurbrillance }"
    >
      <h2 class="documents__groupe-title">
        {{ groupe.candidature?.poste }} — {{ groupe.candidature?.organisme }}
      </h2>

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
              <CspBadge
                v-if="doc.obligatoire"
                label="Obligatoire"
                size="sm"
                variant="outline"
              />
            </p>
            <p class="documents__item-raison">
              {{ doc.raison }}
            </p>
            <p class="documents__item-meta">
              Étape : {{ doc.etape }} · Visible par {{ doc.visiblePar }}
            </p>
          </div>

          <CspBadge
            v-if="doc.statut === 'fourni'"
            label="Fourni"
            type="success"
            variant="soft"
          />
          <CspButton
            v-else
            variant="secondary"
            size="sm"
            label="Ajouter le document"
            @click="deposerDocument(doc.id)"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
.documents {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.documents__title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.documents__groupe {
  border-radius: 0.375rem;
  padding: var(--csp-space-4);

  &--surligne {
    box-shadow: 0 0 0 2px var(--border-action-high-blue-france);
  }
}

.documents__groupe-title {
  margin: 0 0 var(--csp-space-3);
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.documents__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.documents__item {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
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
  gap: 0.125rem;
}

.documents__item-nom {
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.documents__item-raison {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-default-grey);
}

.documents__item-meta {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
