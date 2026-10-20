import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffreSimple from './variants/simplifie/CreationOffreSimple.vue'

// Version simplifiée : 4 étapes communes à tous, options repliées, validation dans le volet « Suivi ».
// Mêmes données fictives que l'itération 1 (data/scenario.ts). Analyse et hypothèses : NOTES.md.
const meta = {
  title: 'Prototypes/Création d\'offre/Version simplifiée',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Un parcours commun en 4 étapes ; les informations conditionnelles apparaissent selon le contexte, '
          + 'les fonctionnalités avancées restent repliées, la validation est appliquée selon le paramétrage de l\'organisation. '
          + 'Les encadrés « Simulation » remplacent les actions des autres personnes.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(preset: string): Story['render'] {
  return () => ({
    components: { CreationOffreSimple },
    setup: () => ({ preset }),
    template: '<CreationOffreSimple :preset="preset" />',
  })
}

export const Nouvelle: Story = {
  name: '0. Nouvelle offre (organisation avec DAR et validation)',
  render: story('nouveau'),
}

export const Brouillon: Story = {
  name: '1. Brouillon repris',
  render: story('incomplet'),
}

export const EnValidation: Story = {
  name: '2. En validation',
  render: story('a_valider'),
}

export const ACorriger: Story = {
  name: '3. Corrections demandées',
  render: story('a_corriger'),
}

export const PretAPublier: Story = {
  name: '4. Validée, prête à publier',
  render: story('pret'),
}

export const SansValidation: Story = {
  name: '5. Organisation sans circuit de validation (publication directe)',
  render: story('sans_validation'),
}
