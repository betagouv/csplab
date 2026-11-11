<script setup lang="ts">
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { ref } from 'vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'

interface Section {
  id: string
  label: string
}

interface DocumentRow {
  id: string
  name: string
  date: string
}

const sections = ref<Section[]>([
  { id: 'introduction', label: 'Introduction' },
  { id: 'contexte', label: 'Contexte' },
  { id: 'conclusion', label: 'Conclusion' },
])

function onReorder(next: Section[]) {
  sections.value = next
}

const ROWS: DocumentRow[] = [
  { id: '1', name: 'Rapport annuel', date: '03/11/2026' },
  { id: '2', name: 'Budget prévisionnel', date: '28/10/2026' },
  { id: '3', name: 'Compte rendu', date: '14/10/2026' },
]

const COLUMNS: CspColumnDef<DocumentRow>[] = [
  { id: 'name', header: 'Nom', accessor: row => row.name },
  { id: 'date', header: 'Date', align: 'end', accessor: row => row.date },
]

const FILES = ['rapport-annuel.pdf', 'budget-previsionnel.xlsx', 'compte-rendu.docx']
</script>

<template>
  <div class="ecarts-blocs">
    <CspCard
      title="Rapport annuel"
      description="Mis à jour le 3 novembre 2026"
      size="sm"
    />

    <CspSortableList
      :items="sections"
      :get-item-key="item => item.id"
      :get-item-label="item => item.label"
      @reorder="onReorder"
    >
      <template #item="{ item }">
        <span class="ecarts-blocs__grow">{{ item.label }}</span>
      </template>
    </CspSortableList>

    <CspDataTable
      :rows="ROWS"
      :columns="COLUMNS"
      :row-key="row => row.id"
      caption="Documents"
      size="sm"
    />

    <ul class="ecarts-blocs__list">
      <li
        v-for="file in FILES"
        :key="file"
        class="ecarts-blocs__list-item"
      >
        {{ file }}
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.ecarts-blocs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
}

.ecarts-blocs__grow {
  flex: 1;
}

// Same frame as .candidature-documents__list (features/candidatures/components/CandidatureDocuments.vue)
.ecarts-blocs__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
}

.ecarts-blocs__list-item {
  padding: var(--csp-space-3) var(--csp-space-4);
  color: var(--text-default-grey);
  font-size: var(--csp-font-size-sm);

  & + & {
    border-top: 1px solid var(--border-default-grey);
  }
}
</style>
