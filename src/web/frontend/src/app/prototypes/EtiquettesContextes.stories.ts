import type { Meta, StoryObj } from '@storybook/vue3-vite'
import EtiquettesContextes from './EtiquettesContextes.vue'

const meta = {
  title: 'Prototypes/Étiquettes/Contextes',
  component: EtiquettesContextes,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Paramètres de l’organisme, panneaux d’ajout et de modification d’une étiquette, équipe de recrutement, et une rangée qui place une étiquette de chaque couleur à côté des badges de statut, des tags de filtre et d’un bouton.',
      },
    },
  },
} satisfies Meta<typeof EtiquettesContextes>

export default meta

type Story = StoryObj<typeof meta>

export const Contextes: Story = {}
