import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffre from './variants/parcours/CreationOffre.vue'

// Parcours de création d'offre de l'ATS, cliquable de bout en bout.
// Prototype isolé : pas d'API, pas de router — données fictives dans data/scenario.ts.
// Chaque story ouvre le même parcours dans un état différent ; tout reste manipulable.
const meta = {
  title: 'Prototypes/Création d\'offre/Itération 1 (archive)',
  id: 'prototypes-creation-offre-v1',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Première itération, jugée trop complexe (8 étapes, alertes permanentes). Conservée pour comparaison. '
          + 'Scénario fictif : la DREAL Occitanie remplace une chargée de mission (DAR validée). '
          + 'Les encadrés « Simulation » remplacent les actions des autres personnes (valideur, contributeur). '
          + 'Hypothèses et questions ouvertes : NOTES.md.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(preset: string): Story['render'] {
  return () => ({
    components: { CreationOffre },
    setup: () => ({ preset }),
    template: '<CreationOffre :preset="preset" />',
  })
}

export const Demarrage: Story = {
  name: '0. Scénario complet — démarrer une offre',
  render: story('nouveau'),
}

export const Brouillon: Story = {
  name: '1. Brouillon incomplet (reprise après interruption)',
  render: story('incomplet'),
}

export const EnValidation: Story = {
  name: '2. En validation',
  render: story('a_valider'),
}

export const ACorriger: Story = {
  name: '3. À corriger (remarques du manager)',
  render: story('a_corriger'),
}

export const PretAPublier: Story = {
  name: '4. Validée — prête à publier',
  render: story('pret'),
}

export const SansDar: Story = {
  name: '5. Autre organisation — circuit court, sans DAR (territoriale)',
  render: story('sans_dar'),
}
