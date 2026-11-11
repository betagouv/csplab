import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsBlocsScene from './EcartsBlocsScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-blocs--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-blocs--tout-arrondi', label: 'Tout à 0,25 rem' },
  { storyId: 'prototypes-ecarts-blocs--tout-droit', label: 'Tout à angles droits' },
]

const meta = {
  id: 'prototypes-ecarts-blocs',
  title: 'Prototypes/Écarts du kit/Blocs encadrés',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsBlocsScene },
    template: '<EcartsBlocsScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="448" :height="640" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const ToutArrondi: Story = {
  name: 'Tout à 0,25 rem',
  decorators: [withEcart('blocs-tout-arrondi')],
}

export const ToutDroit: Story = {
  name: 'Tout à angles droits',
  decorators: [withEcart('blocs-tout-droit')],
}
