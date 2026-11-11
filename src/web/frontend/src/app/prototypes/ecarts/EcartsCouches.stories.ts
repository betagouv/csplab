import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsCouchesScene from './EcartsCouchesScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-couches--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-couches--tout-arrondi', label: 'Tout à 0,25 rem' },
  { storyId: 'prototypes-ecarts-couches--tout-droit', label: 'Tout à angles droits' },
]

const meta = {
  id: 'prototypes-ecarts-couches',
  title: 'Prototypes/Écarts du kit/Couches proches',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsCouchesScene },
    template: '<EcartsCouchesScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="448" :height="620" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const ToutArrondi: Story = {
  name: 'Tout à 0,25 rem',
  decorators: [withEcart('couches-tout-arrondi')],
}

export const ToutDroit: Story = {
  name: 'Tout à angles droits',
  decorators: [withEcart('couches-tout-droit')],
}
