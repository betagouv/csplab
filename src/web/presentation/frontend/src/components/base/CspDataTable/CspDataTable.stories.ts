import type { ComponentPropsAndSlots, Meta, StoryObj } from '@storybook/vue3-vite'
import type { CspColumnDef } from './table'
import { computed, reactive, ref } from 'vue'
import CspPagination from '@/components/base/CspPagination/CspPagination.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspDataTable from './CspDataTable.vue'

type CspDataTableProps = ComponentPropsAndSlots<typeof CspDataTable>

interface DemoRow {
  id: string
  libelle: string
  reference: string
  categorie: string
  date: string
  quantite: number
}

interface StateDemo {
  name: string
  rows: DemoRow[]
  size: CspDataTableProps['size']
  selectionMode: CspDataTableProps['selectionMode']
  emptyLabel?: string
}

const DEMO_ROWS: DemoRow[] = [
  { id: '1', libelle: 'Alpha', reference: 'REF-001', categorie: 'Catégorie A', date: '15/02/26', quantite: 24 },
  { id: '2', libelle: 'Bravo', reference: 'REF-002', categorie: 'Catégorie B', date: '12/02/26', quantite: 18 },
  { id: '3', libelle: 'Charlie', reference: 'REF-003', categorie: 'Catégorie A', date: '10/02/26', quantite: 31 },
  { id: '4', libelle: 'Delta', reference: 'REF-004', categorie: 'Catégorie C', date: '08/02/26', quantite: 12 },
  { id: '5', libelle: 'Echo', reference: 'REF-005', categorie: 'Catégorie B', date: '05/02/26', quantite: 27 },
  { id: '6', libelle: 'Foxtrot', reference: 'REF-006', categorie: 'Catégorie A', date: '03/02/26', quantite: 9 },
  { id: '7', libelle: 'Golf', reference: 'REF-007', categorie: 'Catégorie C', date: '01/02/26', quantite: 15 },
  { id: '8', libelle: 'Hotel', reference: 'REF-008', categorie: 'Catégorie B', date: '29/01/26', quantite: 22 },
]

const SHORT_ROWS = DEMO_ROWS.slice(0, 4)

const COLUMNS: CspColumnDef<DemoRow>[] = [
  { id: 'libelle', header: 'Libellé', sortable: true, width: '26%', accessor: row => row.libelle },
  { id: 'reference', header: 'Référence', sortable: true, width: '18%', accessor: row => row.reference },
  { id: 'categorie', header: 'Catégorie', sortable: true, width: '22%', accessor: row => row.categorie },
  { id: 'date', header: 'Date', sortable: true, width: '16%', accessor: row => row.date },
  { id: 'quantite', header: 'Quantité', sortable: true, align: 'end', width: '18%', accessor: row => row.quantite },
]

function createSelectionState() {
  const selectedIds = ref<Set<string>>(new Set())
  const count = computed(() => selectedIds.value.size)

  function toggle(id: string): void {
    const next = new Set(selectedIds.value)
    if (next.has(id)) {
      next.delete(id)
    }
    else {
      next.add(id)
    }
    selectedIds.value = next
  }

  function toggleVisible(visibleIds: string[]): void {
    const allSelected = visibleIds.length > 0 && visibleIds.every(id => selectedIds.value.has(id))
    const next = new Set(selectedIds.value)

    if (allSelected) {
      visibleIds.forEach(id => next.delete(id))
    }
    else {
      visibleIds.forEach(id => next.add(id))
    }

    selectedIds.value = next
  }

  return {
    count,
    selectedIds,
    toggle,
    toggleVisible,
  }
}

function createStateGalleryRender(demos: StateDemo[]) {
  return () => ({
    components: { CspDataTable, CspTag },
    setup() {
      return {
        columns: COLUMNS,
        demos: reactive(demos.map((demo) => {
          const selection = createSelectionState()

          return {
            ...demo,
            count: selection.count,
            selectedIds: selection.selectedIds,
            onToggleRow: (id: string) => selection.toggle(id),
            onToggleAll: (ids: string[]) => selection.toggleVisible(ids),
          }
        })),
      }
    },
    template: `
      <div class="grid max-w-6xl gap-6">
        <section
          v-for="demo in demos"
          :key="demo.name"
          class="grid gap-3"
        >
          <div class="flex flex-wrap items-center justify-between gap-3">
            <p class="m-0 text-sm font-medium text-[var(--text-title-grey)]">{{ demo.name }}</p>
            <p
              v-if="demo.selectionMode !== 'none'"
              class="m-0 text-sm text-[var(--text-mention-grey)]"
            >
              {{ demo.count }} sélectionnée(s)
            </p>
          </div>

          <CspDataTable
            :rows="demo.rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données"
            :selection-mode="demo.selectionMode"
            :selected-ids="demo.selectedIds"
            :selection-label="(row) => 'Sélectionner ' + row.libelle"
            :size="demo.size"
            :empty-label="demo.emptyLabel"
            @toggle-row="demo.onToggleRow"
            @toggle-all="demo.onToggleAll"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
            <template #cell-quantite="{ value }">
              <strong>{{ value }}</strong>
            </template>
          </CspDataTable>
        </section>
      </div>
    `,
  })
}

const meta = {
  title: 'Compositions/Génériques/CspDataTable',
  component: CspDataTable as unknown as Meta['component'],
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
    controls: {
      include: ['selectionMode', 'size', 'pageSize'],
    },
    docs: {
      description: {
        component: 'Table de données générique avec tri, densité, pagination et sélection. Les cellules riches passent par les slots `cell-*`, les en-têtes par `header-*`, et le footer reçoit le contexte de pagination.',
      },
    },
  },
  argTypes: {
    selectionMode: {
      control: { type: 'radio' },
      options: ['none', 'checkbox', 'row'] satisfies NonNullable<CspDataTableProps['selectionMode']>[],
      description: 'Mode de sélection des lignes : aucun, case à cocher uniquement, ou clic sur toute la ligne.',
      table: { defaultValue: { summary: 'none' } },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspDataTableProps['size']>[],
      description: 'Densité d’affichage des lignes.',
      table: { defaultValue: { summary: 'default' } },
    },
    pageSize: {
      control: { type: 'number', min: 1, step: 1 },
      description: 'Nombre de lignes affichées par page.',
      table: { defaultValue: { summary: '5' } },
    },
  },
  args: {
    selectionMode: 'row',
    size: 'md',
    pageSize: 5,
  },
  render: args => ({
    components: { CspDataTable, CspPagination, CspTag },
    setup() {
      const selection = createSelectionState()

      return {
        args,
        columns: COLUMNS,
        count: selection.count,
        rows: DEMO_ROWS,
        selectedIds: selection.selectedIds,
        onToggleRow: (id: string) => selection.toggle(id),
        onToggleAll: (ids: string[]) => selection.toggleVisible(ids),
      }
    },
    template: `
      <div class="flex max-w-6xl flex-col gap-3">
        <div class="flex flex-wrap items-center gap-4 text-sm text-[var(--text-mention-grey)]">
          <span>{{ count }} sélectionnée(s)</span>
        </div>

        <CspDataTable
          :rows="rows"
          :columns="columns"
          :row-key="(row) => row.id"
          caption="Tableau de données"
          :selection-mode="args.selectionMode"
          :selected-ids="selectedIds"
          :selection-label="(row) => 'Sélectionner ' + row.libelle"
          :size="args.size"
          :page-size="args.pageSize"
          @toggle-row="onToggleRow"
          @toggle-all="onToggleAll"
        >
          <template #cell-categorie="{ value }">
            <CspTag :label="String(value)" variant="static" size="sm" />
          </template>
          <template #cell-quantite="{ value }">
            <strong>{{ value }}</strong>
          </template>
          <template #footer="pg">
            <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <p class="m-0 text-sm text-[var(--text-mention-grey)]">
                Affichage de {{ pg.range.from }} à {{ pg.range.to }} sur {{ pg.total }} éléments
              </p>
              <CspPagination
                :page="pg.page"
                :page-count="pg.pageCount"
                :show-direction-labels="false"
                @update:page="pg.setPage"
              />
            </div>
          </template>
        </CspDataTable>
      </div>
    `,
  }),
} satisfies Meta

export default meta
type Story = StoryObj

export const DefaultDemo: Story = {
  name: 'Par défaut',
}

export const Sizes: Story = {
  name: 'Tailles',
  render: () => ({
    components: { CspDataTable, CspTag },
    setup() {
      return {
        columns: COLUMNS,
        rows: SHORT_ROWS,
        sizes: ['sm', 'md', 'lg'] as const,
      }
    },
    template: `
      <div class="grid max-w-6xl gap-6">
        <section
          v-for="s in sizes"
          :key="s"
          class="grid gap-3"
        >
          <p class="m-0 text-sm font-medium text-[var(--text-title-grey)]">{{ s }}</p>
          <CspDataTable
            :rows="rows"
            :columns="columns"
            :row-key="(row) => row.id"
            caption="Tableau de données"
            :size="s"
          >
            <template #cell-categorie="{ value }">
              <CspTag :label="String(value)" variant="static" size="sm" />
            </template>
            <template #cell-quantite="{ value }">
              <strong>{{ value }}</strong>
            </template>
            <template #footer="pg">
              <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <p class="m-0 text-sm text-[var(--text-mention-grey)]">
                  Affichage de {{ pg.range.from }} à {{ pg.range.to }} sur {{ pg.total }} éléments
                </p>
                <CspPagination
                  :page="pg.page"
                  :page-count="pg.pageCount"
                  :show-direction-labels="false"
                  @update:page="pg.setPage"
                />
              </div>
            </template>
          </CspDataTable>
        </section>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        story: 'Compare rapidement les trois densités supportées par la table.',
      },
    },
  },
}

export const StateVariants: Story = {
  name: 'Modes de sélection',
  render: createStateGalleryRender([
    {
      name: 'Aucune sélection',
      rows: DEMO_ROWS.slice(0, 5),
      size: 'md',
      selectionMode: 'none',
    },
    {
      name: 'Sélection par checkbox',
      rows: DEMO_ROWS.slice(0, 5),
      size: 'md',
      selectionMode: 'checkbox',
    },
    {
      name: 'Sélection par ligne',
      rows: DEMO_ROWS.slice(0, 5),
      size: 'md',
      selectionMode: 'row',
    },
    {
      name: 'État vide',
      rows: [],
      size: 'md',
      selectionMode: 'none',
      emptyLabel: 'Aucun élément',
    },
  ]),
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        story: 'Compare les trois comportements de sélection attendus : aucun, checkbox uniquement, ou sélection par clic sur toute la ligne.',
      },
    },
  },
}
