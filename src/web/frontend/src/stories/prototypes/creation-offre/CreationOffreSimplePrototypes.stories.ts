import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffreSimple from './variants/simplifie/CreationOffreSimple.vue'

// Processus rendu visible : déclaration du besoin (fiche de poste) → validation par DAR ou non
// → rédaction de l'offre → publication. Deux pages : « Mes besoins en recrutement » et « Mes offres ».
// Les données sont conservées pendant la session (sessionStorage). Hypothèses : NOTES.md.
const meta = {
  title: 'Prototypes/Création d\'offre/Version simplifiée',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Partir de « Mes besoins en recrutement » : déclarer un besoin, le faire valider par une DAR ou non, rédiger l\'offre, '
          + 'la créer puis activer ou non sa publication. Les encadrés « Simulation » remplacent les actions des autres personnes.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(props: Record<string, unknown>): Story['render'] {
  return () => ({
    components: { CreationOffreSimple },
    setup: () => ({ props }),
    template: '<CreationOffreSimple v-bind="props" />',
  })
}

export const Besoins: Story = {
  name: '0. Mes besoins en recrutement',
  render: story({ page: 'besoins' }),
}

export const Offres: Story = {
  name: '1. Mes offres',
  render: story({ page: 'offres' }),
}

export const BesoinDarValidee: Story = {
  name: '2. Besoin validé par DAR → rédiger l\'offre (paie, 3 postes)',
  render: story({ ouvrir: 'OFF-2026-0151', vue: 'besoin' }),
}

export const BesoinSansDar: Story = {
  name: '3. Besoin sans DAR → offre en rédaction',
  render: story({ ouvrir: 'OFF-2026-0154', vue: 'offre' }),
}

export const BesoinEnDeclaration: Story = {
  name: '4. Besoin en cours de déclaration (DAR en brouillon)',
  render: story({ ouvrir: 'OFF-2026-0153', vue: 'besoin' }),
}

export const DarSoumise: Story = {
  name: '5. DAR soumise, en attente de validation',
  render: story({ ouvrir: 'OFF-2026-0152', vue: 'besoin' }),
}

export const OffreNonPubliee: Story = {
  name: '6. Offre créée, non publiée',
  render: story({ ouvrir: 'OFF-2026-0141', vue: 'offre' }),
}
