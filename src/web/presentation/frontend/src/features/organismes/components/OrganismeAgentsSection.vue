<script setup lang="ts">
import { useQuery } from '@pinia/colada'
import { computed, ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { pluralize } from '@/utils/format'
import { ORGANISME_AGENTS_COLUMNS } from '../columns'
import { organismeAgentsQuery } from '../queries'

const props = defineProps<{
  organismeUuid: string
}>()

const PAGE_SIZE = 8

const query = useQuery(() => organismeAgentsQuery({ organismeUuid: props.organismeUuid }))

const showSkeleton = useMinimumPending(query.isPending)

const page = ref(1)

const rows = computed(() => query.data.value ?? [])

const { search, filtered } = useTextSearch(rows, row => [`${row.prenom} ${row.nom}`, row.email])

watch(filtered, () => {
  page.value = 1
})

const countLabel = computed(() => {
  const count = filtered.value.length
  return `${count} ${pluralize(count, 'membre')}`
})
</script>

<template>
  <section class="organisme-agents-section">
    <div class="organisme-agents-section__intro">
      <h2 class="organisme-agents-section__title">
        Membres de l'organisme
      </h2>
      <p class="organisme-agents-section__description">
        Participent aux recrutements sur les offres auxquelles ils sont rattachés,
        selon les droits qui leur sont attribués.
      </p>
    </div>

    <CspAsyncSection
      :pending="showSkeleton"
      :error="query.error.value"
      loading-label="Chargement des membres"
      error-title="Impossible de charger les membres"
    >
      <template #skeleton>
        <CspSkeletonTable
          :rows="PAGE_SIZE"
          :columns="ORGANISME_AGENTS_COLUMNS.length"
          with-footer
        />
      </template>

      <div class="organisme-agents-section__header">
        <p class="organisme-agents-section__count">
          {{ countLabel }}
        </p>
        <CspInput
          v-model="search"
          type="search"
          aria-label="Rechercher un membre, un courriel"
          placeholder="Rechercher un membre, un courriel"
          class="organisme-agents-section__search"
        />
      </div>
      <CspDataTable
        v-model:page="page"
        :rows="filtered"
        :columns="ORGANISME_AGENTS_COLUMNS"
        :row-key="row => row.agent_id"
        caption="Membres de l'organisme"
        empty-label="Aucun membre"
        :page-size="PAGE_SIZE"
      />
    </CspAsyncSection>
  </section>
</template>

<style scoped lang="scss">
.organisme-agents-section__intro {
  margin-bottom: var(--csp-space-6);
}

.organisme-agents-section__title {
  font-weight: 600;
  margin: 0 0 var(--csp-space-2);
  font-size: 1.125rem;
}

.organisme-agents-section__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.organisme-agents-section__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--csp-space-4);
}

.organisme-agents-section__count {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.organisme-agents-section__search {
  min-width: 20rem;
  margin-bottom: var(--csp-space-4);
}
</style>
