import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsControlesScene from './EcartsControlesScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-controles--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-controles--segmente-droit', label: 'Contrôle segmenté à angles droits' },
  { storyId: 'prototypes-ecarts-controles--boutons-arrondis', label: 'Boutons à 0,25 rem' },
]

const meta = {
  id: 'prototypes-ecarts-controles',
  title: 'Prototypes/Écarts du kit/Contrôles',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsControlesScene },
    template: '<EcartsControlesScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="448" :height="200" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const SegmenteDroit: Story = {
  name: 'Contrôle segmenté à angles droits',
  decorators: [withEcart('controles-segmente-droit')],
}

export const BoutonsArrondis: Story = {
  name: 'Boutons à 0,25 rem',
  decorators: [withEcart('controles-boutons-arrondis')],
}
