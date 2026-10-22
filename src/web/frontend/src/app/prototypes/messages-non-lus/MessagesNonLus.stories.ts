import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import MessagesNonLusComparaison from './MessagesNonLusComparaison.vue'

const meta = {
  title: 'Prototypes/Messages non lus',
  component: MessagesNonLusComparaison,
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
    docs: {
      description: {
        component: 'Les mêmes cartes du kanban avec chaque façon de signaler une conversation non lue. Le réglage « Non lus » de la barre d’outils applique une variante aux écrans de `Prototypes/Écrans`.',
      },
    },
  },
} satisfies Meta<typeof MessagesNonLusComparaison>

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {}

export const ComparaisonRouge: Story = {
  name: 'Comparaison, signal rouge',
  globals: { nonLusCouleur: 'rouge' },
}
