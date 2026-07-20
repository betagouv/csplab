import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSkeletonSortableList from '@/components/base/CspSkeleton/CspSkeletonSortableList.vue'

type CspSkeletonSortableListProps = ComponentPropsAndSlots<typeof CspSkeletonSortableList>

const meta = {
  title: 'Éléments/Génériques/CspSkeletonSortableList',
  component: CspSkeletonSortableList,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['rows'],
    },
    docs: {
      description: {
        component: 'Skeleton d\'une CspSortableList : réserve l\'encombrement des items détachés (poignée, position, libellé, badge, actions) pendant le chargement.',
      },
    },
  },
  argTypes: {
    rows: {
      control: { type: 'number' },
      description: 'Nombre d\'items.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '6',
        },
      },
    },
  },
}

export default meta
type Story = StoryObj<CspSkeletonSortableListProps>

export const Default: Story = {
  name: 'Par défaut',
  args: {
    rows: 6,
  },
}
