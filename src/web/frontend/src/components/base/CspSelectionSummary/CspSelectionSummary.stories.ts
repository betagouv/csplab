import type { StoryObj } from '@storybook/vue3-vite'
import CspSelectionSummary from '@/components/base/CspSelectionSummary/CspSelectionSummary.vue'

const meta = {
  title: 'Éléments/Génériques/CspSelectionSummary',
  component: CspSelectionSummary,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Résumé d\'une sélection en lot, en tête du panneau d\'une action : une phrase qui donne la portée et le nombre d\'éléments, puis « Modifier la sélection », qui émet `edit` ; la vue ferme alors le panneau.',
      },
    },
  },
  argTypes: {
    summary: {
      control: { type: 'text' },
      description: 'Phrase qui donne la portée de la sélection.',
      table: { type: { summary: 'string' } },
    },
  },
  args: {
    summary: '12 éléments, dont 4 sur d\'autres pages',
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: 'Par défaut',
}
