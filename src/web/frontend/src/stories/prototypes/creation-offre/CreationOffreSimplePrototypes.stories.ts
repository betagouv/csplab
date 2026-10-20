import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffreSimple from './variants/simplifie/CreationOffreSimple.vue'

// Version simplifiée (itérations 2 à 4) : la fiche de poste nourrit la DAR, la DAR validée nourrit l'offre,
// l'offre se retravaille sans toucher à la DAR. 4 étapes, sauvegarde automatique, publication activable à part.
// Les recrutements ouverts depuis la liste sont conservés pendant la session (sessionStorage).
const meta = {
  title: 'Prototypes/Création d\'offre/Version simplifiée',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Scénario principal : à partir de la DAR validée DAR-2026-0331 (3 postes de gestionnaire de paie), créer l\'offre, '
          + 'reformuler le texte brut de la DAR, quitter puis reprendre, créer l\'offre sans activer la publication. '
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
  name: '0. Recrutements (liste, point de départ)',
  render: story({ liste: true }),
}

export const DepuisDar: Story = {
  name: '1. Scénario principal — offre depuis une DAR validée (paie, 3 postes)',
  render: story({ depuisDar: 'DAR-2026-0331' }),
}

export const DarSoumise: Story = {
  name: '2. DAR soumise — préparer l\'offre en attendant la validation',
  render: story({ depuisDar: 'DAR-2026-0322' }),
}

export const DarBrouillon: Story = {
  name: '3. DAR en brouillon — préparée depuis la fiche de poste',
  render: story({ depuisDar: 'DAR-2026-0335' }),
}

export const OffreCreee: Story = {
  name: '4. Offre créée, publication désactivée',
  render: story({ ouvrir: 'OFF-2026-0141' }),
}

export const ValidationOffre: Story = {
  name: '5. Autre organisation — l\'offre est aussi validée (démo isolée)',
  render: story({ preset: 'a_valider' }),
}
