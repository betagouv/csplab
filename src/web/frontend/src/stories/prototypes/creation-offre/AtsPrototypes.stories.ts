import type { StoryObj } from '@storybook/vue3-vite'
import AtsApp from './variants/ats/AtsApp.vue'

// Deux objets distincts et reliés : la fiche de poste (référentiel durable) et l'offre d'emploi
// (opération de recrutement + annonce destinée aux candidats). Données fictives, conservées pendant la session.
const meta = {
  title: 'Prototypes/Création d\'offre/ATS — fiches de poste et offres',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Tableau de bord, référentiel des fiches (origines ATS, SIRH, document), offres d\'emploi (5 états, DAR conditionnelle), '
          + 'création en 4 modes toujours rattachée à une fiche, rédaction avec aide et aperçu candidat. Hypothèses : NOTES.md.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(depart: Record<string, unknown>): Story['render'] {
  return () => ({
    components: { AtsApp },
    setup: () => ({ depart }),
    template: '<AtsApp :depart="depart" />',
  })
}

export const Accueil: Story = { name: '1. Tableau de bord', render: story({ nom: 'accueil' }) }
export const Fiches: Story = { name: '2. Fiches de poste', render: story({ nom: 'fiches' }) }
export const FichePaie: Story = { name: '3. Détail — fiche « Gestionnaire de paie » (ATS)', render: story({ nom: 'fiche', id: 'FP-SG-2026-007' }) }
export const FicheSirh: Story = { name: '3 bis. Détail — fiche « Chargé·e de recrutement » (SIRH)', render: story({ nom: 'fiche', id: 'FP-SIRH-48213' }) }
export const Creation: Story = { name: '4. Créer une offre — 4 modes', render: story({ nom: 'creation' }) }
export const Redaction: Story = { name: '5. Rédaction — offre « Gestionnaire de paie » (3 postes)', render: story({ nom: 'offre', id: 'OFF-2026-0151', onglet: 'redaction' }) }
export const Validation: Story = { name: '6. Validation (DAR) — offre « Chargé·e de recrutement »', render: story({ nom: 'offre', id: 'OFF-2026-0148', onglet: 'publication' }) }
export const APublier: Story = { name: '6 bis. À publier — offre « Chef·fe de projet numérique »', render: story({ nom: 'offre', id: 'OFF-2026-0145', onglet: 'publication' }) }
export const Suivi: Story = { name: '7. Suivi — offre publiée « Assistant·e administratif·ve »', render: story({ nom: 'offre', id: 'OFF-2026-0118' }) }
export const Offres: Story = { name: '8. Offres d\'emploi', render: story({ nom: 'offres' }) }
