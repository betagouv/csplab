import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import EtiquettesFormes from './EtiquettesFormes.vue'

const meta = {
  title: 'Prototypes/Étiquettes/Formes',
  component: EtiquettesFormes,
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
} satisfies Meta<typeof EtiquettesFormes>

export default meta

type Story = StoryObj<typeof meta>

export const Formes: Story = {}
