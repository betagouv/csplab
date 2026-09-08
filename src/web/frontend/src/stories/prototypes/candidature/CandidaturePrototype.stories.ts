import type { StoryObj } from '@storybook/vue3-vite'
import PrototypeApp from './shared/PrototypeApp.vue'

const meta = {
  title: 'Prototypes/Panneau de candidature',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Expérience cible du panneau de candidature ouvert depuis le kanban : en-tête, onglets, '
          + 'colonne de droite (activités, tags, note), navigation dans la colonne, changement d\'étape '
          + 'avec son message de confirmation, garde-fou sur une saisie en cours et écran d\'accès refusé. '
          + 'Les données sont fictives et vivent dans la page : recharger la story remet tout à zéro.',
      },
    },
  },
}

export default meta
type Story = StoryObj

export const Parcours: Story = {
  name: 'Parcours depuis le kanban',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp />',
  }),
}

export const PremiereCandidature: Story = {
  name: 'Ouvert sur la première candidature',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp initial-open="premiere" />',
  }),
}

export const DerniereDeLaColonne: Story = {
  name: 'Cas limite/Dernière candidature de la colonne',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp initial-open="derniere" />',
  }),
}

export const SansCv: Story = {
  name: 'Cas limite/Candidature sans CV',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp initial-open="sans-cv" />',
  }),
}

export const CvIllisible: Story = {
  name: 'Cas limite/CV impossible à afficher',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp initial-open="cv-illisible" />',
  }),
}

export const AccesRefuse: Story = {
  name: 'Cas limite/Accès refusé',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp acces-refuse />',
  }),
}
