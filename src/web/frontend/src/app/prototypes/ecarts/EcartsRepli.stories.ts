import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { EcartsPlancheFrame } from './EcartsPlanche.vue'
import { withDesktopSidebar, withEcart } from './ecarts-stories'
import EcartsPlanche from './EcartsPlanche.vue'
import EcartsRepliScene from './EcartsRepliScene.vue'
import './ecarts.css'

const FRAMES: EcartsPlancheFrame[] = [
  { storyId: 'prototypes-ecarts-repli--aujourdhui', label: 'Aujourd\'hui' },
  { storyId: 'prototypes-ecarts-repli--comme-ses-voisins', label: 'Bouton de repli dessiné comme ses voisins' },
]

const meta = {
  id: 'prototypes-ecarts-repli',
  title: 'Prototypes/Écarts du kit/Bouton de repli de la barre latérale',
  parameters: {
    layout: 'fullscreen',
  },
  render: () => ({
    components: { EcartsRepliScene },
    template: '<EcartsRepliScene />',
  }),
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

export const Planche: Story = {
  render: () => ({
    components: { EcartsPlanche },
    setup: () => ({ frames: FRAMES }),
    template: '<EcartsPlanche :frames="frames" :width="680" :height="560" />',
  }),
}

export const Aujourdhui: Story = {
  name: 'Aujourd\'hui',
  decorators: [withEcart(), withDesktopSidebar],
}

export const CommeSesVoisins: Story = {
  name: 'Bouton de repli dessiné comme ses voisins',
  decorators: [withEcart('repli-comme-ses-voisins'), withDesktopSidebar],
}
