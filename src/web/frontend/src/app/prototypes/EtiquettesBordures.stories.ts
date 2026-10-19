import type { Meta, StoryObj } from '@storybook/vue3-vite'
import EtiquettesBordures from './EtiquettesBordures.vue'

const meta = {
  title: 'Prototypes/Étiquettes/Bordures',
  component: EtiquettesBordures,
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta<typeof EtiquettesBordures>

export default meta

type Story = StoryObj<typeof meta>

export const Bordures: Story = {}
