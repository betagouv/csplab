import type { StoryObj } from '@storybook/vue3-vite'
import AtsApp from './variants/ats/AtsApp.vue'

// Deux objets distincts et reliés : la fiche de poste (référentiel durable) et l'offre d'emploi.
// Parcours : lancer un recrutement → page unique de l'offre (tout est modifiable) → validation si l'organisme l'exige → publication
// (dates, diffusion) → suivi, prolongation, retrait. Données fictives, conservées pendant la session.
const meta = {
  title: 'Prototypes/Création d\'offre/ATS — fiches de poste et offres',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Aligné sur le cadrage « Offres » : page unique de l\'offre en sections repliables (annonce avec suivi interne, candidature, paramètres, publication, journal) et résumé pour les valideurs, validation (ancienne DAR) demandable à tout moment '
          + 'et paramétrée par le superviseur, publication avec dates de début et de fin. Hypothèses : NOTES.md.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(depart: Record<string, unknown>, validation?: boolean, role?: 'demandeur' | 'valideur'): Story['render'] {
  return () => ({
    components: { AtsApp },
    setup: () => ({ depart, validation, role }),
    template: '<AtsApp :depart="depart" :validation="validation" :role="role" />',
  })
}

export const Accueil: Story = { name: '1. Tableau de bord', render: story({ nom: 'accueil' }) }
export const Fiches: Story = { name: '2. Fiches de poste', render: story({ nom: 'fiches' }) }
export const FichePaie: Story = { name: '3. Fiche « Gestionnaire de paie » → lancer un recrutement', render: story({ nom: 'fiche', id: 'FP-SG-2026-007' }) }
export const Lancer: Story = { name: '4. Lancer un recrutement — 3 sources', render: story({ nom: 'creation' }) }
export const Brouillon: Story = { name: '5. Offre en brouillon — page unique, demander la validation à tout moment', render: story({ nom: 'offre', id: 'OFF-2026-0151' }, true) }
export const EnValidation: Story = { name: '6. Validation en cours — « Chargé·e de recrutement »', render: story({ nom: 'offre', id: 'OFF-2026-0148' }, true) }
export const VueValideur: Story = { name: '6 bis. Vue du valideur (Claire Morel) — lecture seule, Valider ou Refuser', render: story({ nom: 'offre', id: 'OFF-2026-0148' }, true, 'valideur') }
export const APublier: Story = { name: '7. Validée et complète, prête à être publiée — « Chef·fe de projet numérique »', render: story({ nom: 'offre', id: 'OFF-2026-0145' }, true) }
export const Publier: Story = { name: '7 bis. Publier — affichage candidat, dates et diffusion', render: story({ nom: 'apercu', id: 'OFF-2026-0145', publier: true }, true) }
export const Suivi: Story = { name: '8. Offre en ligne qui se termine bientôt — prolonger ou retirer', render: story({ nom: 'offre', id: 'OFF-2026-0118' }) }
export const SansValidation: Story = { name: '8 bis. Organisme sans circuit de validation', render: story({ nom: 'offre', id: 'OFF-2026-0151' }, false) }
export const Parametres: Story = { name: '9. Paramètres de l\'organisme', render: story({ nom: 'parametres' }) }
