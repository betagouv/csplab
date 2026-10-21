import type { StoryObj } from '@storybook/vue3-vite'
import CreationOffreSimple from './variants/simplifie/CreationOffreSimple.vue'

// La fiche de poste comme point d'entrée : référentiel durable → lancer un recrutement (avec DAR ou
// création directe) → création d'offre commune → publication distincte.
// Données conservées pendant la session (sessionStorage). Hypothèses : NOTES.md.
const meta = {
  title: 'Prototypes/Création d\'offre/Archives/Itérations 2 à 6',
  id: 'prototypes-creation-offre-v6',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Scénario : ouvrir la fiche « Gestionnaire de paie », lancer un recrutement de 3 postes avec DAR, enregistrer, soumettre, '
          + 'simuler la validation, créer l\'offre sans activer la publication. Second cas : création directe depuis la fiche « Responsable informatique ».',
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

export const Fiches: Story = {
  name: '0. Fiches de poste (référentiel, point d\'entrée)',
  render: story({ page: 'fiches' }),
}

export const FichePaie: Story = {
  name: '1. Fiche « Gestionnaire de paie » → recrutement avec DAR',
  render: story({ fiche: 'FP-SG-2026-007' }),
}

export const FicheInformatique: Story = {
  name: '2. Fiche « Responsable informatique » → création directe de l\'offre',
  render: story({ fiche: 'FP-SG-2024-031' }),
}

export const Recrutements: Story = {
  name: '3. Recrutements (suivi)',
  render: story({ page: 'recrutements' }),
}

export const Offres: Story = {
  name: '4. Mes offres',
  render: story({ page: 'offres' }),
}

export const DarSoumise: Story = {
  name: '5. Recrutement — DAR soumise (validation à simuler)',
  render: story({ ouvrir: 'REC-2026-0152', vue: 'besoin' }),
}

export const OffreNonPubliee: Story = {
  name: '6. Recrutement — offre créée, non publiée',
  render: story({ ouvrir: 'REC-2026-0141', vue: 'offre' }),
}
