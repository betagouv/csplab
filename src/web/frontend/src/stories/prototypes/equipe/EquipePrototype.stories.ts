import type { StoryObj } from '@storybook/vue3-vite'
import PrototypeApp from './shared/PrototypeApp.vue'

const meta = {
  title: 'Prototypes/Équipe de recrutement',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Expérience cible de la constitution des équipes : attribution des responsables depuis la liste '
          + 'des recrutements (unitaire et en lot), équipe d\'une offre avec ses rôles, invitation à la volée '
          + 'd\'une personne sans compte, membres et journal d\'audit de l\'organisme. Le sélecteur de point de vue '
          + 'en haut de page rejoue le même parcours avec les droits de chaque rôle. '
          + 'Les données sont fictives et vivent dans la page : recharger la story remet tout à zéro.',
      },
    },
  },
}

export default meta
type Story = StoryObj

export const Gestionnaire: Story = {
  name: 'Parcours du gestionnaire',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="gestionnaire" />',
  }),
}

export const Responsable: Story = {
  name: 'Parcours du responsable d\'offre',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="responsable" initial-page="equipe" />',
  }),
}

export const Recruteur: Story = {
  name: 'Point de vue du recruteur',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="recruteur" />',
  }),
}

export const Admin: Story = {
  name: 'Point de vue de l\'administrateur',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="admin" initial-page="organisme" />',
  }),
}

export const MembresOrganisme: Story = {
  name: 'Ouvert sur les membres de l\'organisme',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="gestionnaire" initial-page="organisme" />',
  }),
}

export const SansRecrutement: Story = {
  name: 'Cas limite/Agent sans recrutement',
  render: () => ({
    components: { PrototypeApp },
    template: '<PrototypeApp persona="sans-offre" />',
  }),
}
