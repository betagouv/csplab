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
    editable: {
      control: { type: 'boolean' },
      description: 'Affiche « Modifier la sélection ». Désactivé quand l\'action porte sur un élément choisi depuis sa ligne.',
      table: { type: { summary: 'boolean' }, defaultValue: { summary: 'true' } },
    },
  },
  args: {
    summary: '12 éléments, dont 4 sur d\'autres pages',
    editable: true,
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: 'Par défaut',
}

export const SingleElement: Story = {
  name: 'Élément unique',
  args: {
    summary: 'Élément A',
    editable: false,
  },
}
