<script setup lang="ts">
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { EQUIPE_RECRUTEMENT_COLUMNS } from '../columns'
import { useEquipeRecrutement } from '../composables/useEquipeRecrutement'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const PAGE_SIZE = 8

const { membres, pending, error } = useEquipeRecrutement(props.organismeUuid, props.recrutementUuid)

const showSkeleton = useMinimumPending(pending)
</script>

<template>
  <section class="equipe-recrutement-section">
    <div class="equipe-recrutement-section__intro">
      <h2 class="equipe-recrutement-section__title">
        Membres de l’équipe de recrutement
      </h2>
      <p class="equipe-recrutement-section__description">
        L'équipe de recrutement regroupe les utilisateurs qui participent au traitement
        des candidatures sur cette offre.
      </p>
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement de l'équipe de recrutement"
      error-title="Impossible de charger l'équipe de recrutement"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="EQUIPE_RECRUTEMENT_COLUMNS.length"
          with-footer
        />
      </template>

      <CspDataTable
        :rows="membres"
        :columns="EQUIPE_RECRUTEMENT_COLUMNS"
        :row-key="row => row.agent_id"
        caption="Équipe de recrutement"
        :page-size="PAGE_SIZE"
      >
        <template #empty>
          <div class="equipe-recrutement-section__empty">
            <p class="equipe-recrutement-section__empty-title">
              Aucun membre rattaché à ce recrutement.
            </p>
          </div>
        </template>
      </CspDataTable>
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.equipe-recrutement-section__intro {
  margin-bottom: var(--csp-space-5);
}

.equipe-recrutement-section__title {
  font-weight: 600;
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.equipe-recrutement-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  max-width: 65ch;
}

.equipe-recrutement-section__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6) 0;
}

.equipe-recrutement-section__empty-title {
  margin: 0;
}
</style>
