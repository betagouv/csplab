import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import { RECRUTEMENTS_ACTIFS_COLUMNS, RECRUTEMENTS_ARCHIVES_COLUMNS } from '../columns'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '../mock'

const meta = {
  title: 'Compositions/ATS/Recrutements',
  component: CspDataTable as unknown as Meta['component'],
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'Tables métier des recrutements : CspDataTable composé avec les définitions de colonnes de la feature (columns.ts)',
      },
    },
  },
} satisfies Meta

export default meta
type Story = StoryObj

export const EnCours: Story = {
  name: 'Recrutements en cours',
  render: () => ({
    components: { CspDataTable },
    setup() {
      const page = ref(1)
      return { page, rows: RECRUTEMENTS_ACTIFS, columns: RECRUTEMENTS_ACTIFS_COLUMNS }
    },
    template: `
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.offer_id"
        activation-mode="cell"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      >
        <template #header-candidatures="{ label }">
          <div class="flex flex-col gap-0.5">
            <span>{{ label }}</span>
            <span class="text-xs font-normal text-(--text-mention-grey)"># • À traiter • En cours</span>
          </div>
        </template>
      </CspDataTable>
    `,
  }),
}

export const Archivees: Story = {
  name: 'Offres archivées',
  render: () => ({
    components: { CspDataTable },
    setup() {
      const page = ref(1)
      return { page, rows: RECRUTEMENTS_ARCHIVES, columns: RECRUTEMENTS_ARCHIVES_COLUMNS }
    },
    template: `
      <CspDataTable
        v-model:page="page"
        :rows="rows"
        :columns="columns"
        :row-key="row => row.offer_id"
        activation-mode="cell"
        caption="Offres archivées"
        empty-label="Aucune offre archivée"
        :page-size="10"
      />
    `,
  }),
}

export const EtatVide: Story = {
  name: 'État vide',
  render: () => ({
    components: { CspDataTable },
    setup() {
      return { columns: RECRUTEMENTS_ACTIFS_COLUMNS }
    },
    template: `
      <CspDataTable
        :rows="[]"
        :columns="columns"
        :row-key="row => row.offer_id"
        caption="Recrutements en cours"
        empty-label="Aucun recrutement en cours"
        :page-size="10"
      />
    `,
  }),
}
