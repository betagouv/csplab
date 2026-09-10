import type { StoryObj } from '@storybook/vue3-vite'
import type { Persona } from './data/mock'
import type { InitialPage } from './shared/PrototypeApp.vue'
import { PERSONAS } from './data/mock'
import PrototypeApp from './shared/PrototypeApp.vue'

interface EquipeArgs {
  persona: Persona
}

const PERSONA_LABELS = Object.fromEntries(
  Object.entries(PERSONAS).map(([value, persona]) => [value, `${persona.label} — ${persona.nom}`]),
)

function scene(initialPage: InitialPage) {
  return (args: EquipeArgs) => ({
    components: { PrototypeApp },
    setup: () => ({ args, initialPage }),
    template: '<PrototypeApp :persona="args.persona" :initial-page="initialPage" />',
  })
}

const meta = {
  title: 'Prototypes/Équipe de recrutement',
  args: {
    persona: 'gestionnaire' as Persona,
  },
  argTypes: {
    persona: {
      name: 'Point de vue',
      description: 'Rôle joué pendant le parcours. Les droits, les écrans accessibles et les actions '
        + 'proposées en dépendent. Changer de point de vue conserve les données en cours.',
      control: { type: 'select', labels: PERSONA_LABELS },
      options: Object.keys(PERSONAS),
    },
  },
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Expérience cible de la constitution des équipes : attribution des responsables depuis la liste '
          + 'des recrutements (unitaire et en lot), équipe d\'une offre avec ses rôles, invitation à la volée '
          + 'd\'une personne sans compte, membres et journal d\'audit de l\'organisme. '
          + 'Le contrôle « Point de vue » rejoue le même parcours avec les droits de chaque rôle : '
          + 'gestionnaire, responsable d\'offre, recruteur, agent rattaché à aucun recrutement, '
          + 'administrateur de la plateforme. Les données en cours sont conservées d\'un point de vue à '
          + 'l\'autre, ce qui permet de regarder une équipe que l\'on vient de constituer avec les yeux d\'un '
          + 'autre rôle. Les données sont fictives et vivent dans la page : recharger la story remet tout à zéro.',
      },
    },
  },
}

export default meta
type Story = StoryObj<EquipeArgs>

export const Recrutements: Story = {
  name: 'Liste des recrutements',
  render: scene('recrutements'),
}

export const EquipeOffre: Story = {
  name: 'Équipe d\'une offre',
  render: scene('equipe'),
}

export const MembresOrganisme: Story = {
  name: 'Membres de l\'organisme',
  render: scene('organisme'),
}
