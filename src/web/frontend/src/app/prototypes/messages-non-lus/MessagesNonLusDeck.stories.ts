import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import MessagesNonLusComparaison from './MessagesNonLusComparaison.vue'

const meta = {
  title: 'Prototypes/Messages non lus/Deck',
  component: MessagesNonLusComparaison,
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
    docs: {
      description: {
        component: 'Groupes de variantes cadrés pour les diapositives du deck sur les messages non lus.',
      },
    },
  },
} satisfies Meta<typeof MessagesNonLusComparaison>

export default meta

type Story = StoryObj<typeof meta>

const ROUGE = { nonLusCouleur: 'rouge' }

export const Maquette: Story = {
  args: { variants: ['maquette'] },
}

export const LigneDeLaDate: Story = {
  name: 'Ligne de la date',
  args: { variants: ['maquette', 'maquette-icone', 'icone-date'] },
}

export const LigneDeLaDateRouge: Story = {
  name: 'Ligne de la date, rouge',
  args: LigneDeLaDate.args,
  globals: ROUGE,
}

export const LigneDuNom: Story = {
  name: 'Ligne du nom',
  args: { variants: ['nom-gras', 'point-nom', 'compteur-nom'] },
}

export const LigneDuNomRouge: Story = {
  name: 'Ligne du nom, rouge',
  args: LigneDuNom.args,
  globals: ROUGE,
}

export const BlocAPart: Story = {
  name: 'Bloc à part',
  args: { variants: ['badge-statut', 'pied-lien'] },
}

export const BlocAPartRouge: Story = {
  name: 'Bloc à part, rouge',
  args: BlocAPart.args,
  globals: ROUGE,
}
