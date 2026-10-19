import type { Meta, StoryObj } from '@storybook/vue3-vite'
import PaletteKit from './PaletteKit.vue'

const meta = {
  title: 'Prototypes/Étiquettes/Palette du kit',
  component: PaletteKit,
  globals: { etiquettes: 'kit' },
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Couleur proposée pour une nouvelle étiquette de note, avatars de l’équipe de recrutement et étapes de recrutement, avec la palette du scénario `kit`.',
      },
    },
  },
} satisfies Meta<typeof PaletteKit>

export default meta

type Story = StoryObj<typeof meta>

export const Usages: Story = {
  name: 'Création et autres usages',
}
