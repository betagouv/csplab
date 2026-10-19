import type { Meta, StoryObj } from '@storybook/vue3-vite'
import PaletteUsages from './PaletteUsages.vue'

const meta = {
  title: 'Prototypes/Étiquettes/Autres usages',
  component: PaletteUsages,
  globals: { etiquettes: 'libre' },
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Avatars des membres et pastilles des étapes, dans les couleurs de la palette des étiquettes, à côté du badge de statut d’une colonne du kanban.',
      },
    },
  },
} satisfies Meta<typeof PaletteUsages>

export default meta

type Story = StoryObj<typeof meta>

export const AutresUsages: Story = {
  name: 'Autres usages',
}
