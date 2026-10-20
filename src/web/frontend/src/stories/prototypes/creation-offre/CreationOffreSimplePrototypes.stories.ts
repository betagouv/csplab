import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffreSimple from './variants/simplifie/CreationOffreSimple.vue'

// Version simplifiée (itérations 2 et 3) : liste des offres, 4 étapes communes, options repliées,
// sauvegarde automatique, validation et historique dans le volet « Suivi ».
// Les dossiers ouverts depuis la liste sont conservés pendant la session (sessionStorage).
const meta = {
  title: 'Prototypes/Création d\'offre/Version simplifiée',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Scénario : Camille prépare une offre pour 3 postes de gestionnaire de paie à partir d\'une fiche de poste incomplète, '
          + 'est interrompue, reprend son brouillon, rédige l\'offre sans toucher à la DAR, puis la soumet. '
          + 'Les encadrés « Simulation » remplacent les actions des autres personnes. Hypothèses : NOTES.md.',
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

export const Liste: Story = {
  name: '0. Liste des offres (point de départ du scénario)',
  render: story({ liste: true }),
}

export const BrouillonPaie: Story = {
  name: '1. Brouillon repris — gestionnaires de paie (3 postes)',
  render: story({ ouvrir: 'OFF-2026-0150' }),
}

export const Soumise: Story = {
  name: '2. Soumise à validation',
  render: story({ ouvrir: 'OFF-2026-0141' }),
}

export const ACorriger: Story = {
  name: '3. Corrections demandées',
  render: story({ ouvrir: 'OFF-2026-0139' }),
}

export const PretAPublier: Story = {
  name: '4. Validée, prête à publier (démo isolée)',
  render: story({ preset: 'pret' }),
}

export const SansValidation: Story = {
  name: '5. Organisation sans circuit de validation (démo isolée)',
  render: story({ preset: 'sans_validation' }),
}
