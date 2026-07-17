import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'

type CspSkeletonTableProps = ComponentPropsAndSlots<typeof CspSkeletonTable>

const meta = {
  title: 'Éléments/Génériques/CspSkeletonTable',
  component: CspSkeletonTable,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['rows', 'columns', 'withHeader'],
    },
    docs: {
      description: {
        component: 'Skeleton de tableau : réserve l\'encombrement d\'un CspDataTable pendant le chargement. Dimensionner `rows`/`columns` sur le tableau attendu (ex. la taille de page).',
      },
    },
  },
  argTypes: {
    rows: {
      control: { type: 'number' },
      description: 'Nombre de lignes de données.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '6',
        },
      },
    },
    columns: {
      control: { type: 'number' },
      description: 'Nombre de colonnes.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '4',
        },
      },
    },
    withHeader: {
      control: { type: 'boolean' },
      description: 'Affiche la ligne d\'en-tête.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'true',
        },
      },
    },
  },
}

export default meta
type Story = StoryObj<CspSkeletonTableProps>

export const Default: Story = {
  name: 'Par défaut',
  args: {
    rows: 6,
    columns: 4,
  },
}

export const SansEntete: Story = {
  name: 'Sans en-tête',
  args: {
    rows: 4,
    columns: 3,
    withHeader: false,
  },
}
