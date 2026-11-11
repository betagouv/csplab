import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsGrisScene from './EcartsGrisScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-gris--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-gris--squelette-contraste', label: 'Squelette sur le gris des avatars et badges' },
]

const meta = {
  id: 'prototypes-ecarts-gris',
  title: 'Prototypes/Écarts du kit/Gris neutres',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsGrisScene },
    template: '<EcartsGrisScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="680" :height="540" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const SqueletteContraste: Story = {
  name: 'Squelette sur le gris des avatars et badges',
  decorators: [withEcart('gris-squelette-contraste')],
}
