import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsModalesScene from './EcartsModalesScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-modales--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-modales--dialogue-droit', label: 'Dialogue à angles droits' },
]

const meta = {
  id: 'prototypes-ecarts-modales',
  title: 'Prototypes/Écarts du kit/Couches modales',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsModalesScene },
    template: '<EcartsModalesScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="680" :height="520" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const DialogueDroit: Story = {
  name: 'Dialogue à angles droits',
  decorators: [withEcart('modales-dialogue-droit')],
}
