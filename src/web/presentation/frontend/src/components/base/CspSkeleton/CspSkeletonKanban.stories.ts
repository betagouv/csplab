import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'

type CspSkeletonKanbanProps = ComponentPropsAndSlots<typeof CspSkeletonKanban>

const meta = {
  title: 'Éléments/Génériques/CspSkeletonKanban',
  component: CspSkeletonKanban,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    controls: {
      include: ['columns', 'cards'],
    },
    docs: {
      description: {
        component: 'Skeleton de tableau kanban : réserve l\'encombrement des colonnes et cartes pendant le chargement du board.',
      },
    },
  },
  argTypes: {
    columns: {
      control: { type: 'number' },
      description: 'Nombre de colonnes.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '5',
        },
      },
    },
    cards: {
      control: { type: 'number' },
      description: 'Nombre de cartes par colonne.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '3',
        },
      },
    },
  },
}

export default meta
type Story = StoryObj<CspSkeletonKanbanProps>

export const Default: Story = {
  name: 'Par défaut',
  render: (args: CspSkeletonKanbanProps) => ({
    components: { CspSkeletonKanban },
    setup() {
      return { args }
    },
    template: `
      <div style="height: 100vh; display: flex; padding: 1rem; box-sizing: border-box;">
        <CspSkeletonKanban v-bind="args" />
      </div>
    `,
  }),
}
