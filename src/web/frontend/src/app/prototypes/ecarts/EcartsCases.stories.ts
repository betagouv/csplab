import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withEcart } from './ecarts-stories'
import EcartsCasesScene from './EcartsCasesScene.vue'
import EcartsPlanche from './EcartsPlanche.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-cases--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-cases--bordure-grise', label: 'Bordure grise, bleue une fois coché' },
]

const meta = {
  id: 'prototypes-ecarts-cases',
  title: 'Prototypes/Écarts du kit/Cases et boutons radio',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsCasesScene },
    template: '<EcartsCasesScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="600" :height="330" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart()],
}

export const BordureGrise: Story = {
  name: 'Bordure grise, bleue une fois coché',
  decorators: [withEcart('cases-bordure-grise')],
}
