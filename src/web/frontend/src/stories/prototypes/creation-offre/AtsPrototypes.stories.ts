import type { StoryObj } from '@storybook/vue3-vite'
import AtsApp from './variants/ats/AtsApp.vue'

// Deux objets distincts et reliés : la fiche de poste (référentiel durable) et l'offre d'emploi.
// Parcours : lancer un recrutement (3 sources) → formulaire unique de l'offre → « Envoyer pour validation » si l'organisme
// exige une DAR (sinon « Créer l'offre ») → relecture → publication.
// Données fictives, conservées pendant la session.
const meta = {
  title: 'Prototypes/Création d\'offre/ATS — fiches de poste et offres',
  id: 'prototypes-creation-offre',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'La nécessité d\'une DAR est un paramètre de l\'organisme (page « Paramètres de l\'organisme ») : le parcours de l\'offre '
          + 's\'adapte automatiquement. Hypothèses : NOTES.md.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(depart: Record<string, unknown>, darObligatoire?: boolean): Story['render'] {
  return () => ({
    components: { AtsApp },
    setup: () => ({ depart, darObligatoire }),
    template: '<AtsApp :depart="depart" :dar-obligatoire="darObligatoire" />',
  })
}

export const Accueil: Story = { name: '1. Tableau de bord', render: story({ nom: 'accueil' }) }
export const Fiches: Story = { name: '2. Fiches de poste', render: story({ nom: 'fiches' }) }
export const FichePaie: Story = { name: '3. Fiche « Gestionnaire de paie » → lancer un recrutement', render: story({ nom: 'fiche', id: 'FP-SG-2026-007' }) }
export const Lancer: Story = { name: '4. Lancer un recrutement — 3 sources', render: story({ nom: 'creation' }) }
export const AvecDar: Story = { name: '5. Organisme avec DAR — formulaire « Gestionnaire de paie » → Envoyer pour validation', render: story({ nom: 'offre', id: 'OFF-2026-0151', onglet: 'redaction' }, true) }
export const SansDar: Story = { name: '5 bis. Organisme sans DAR — même formulaire → Créer l\'offre', render: story({ nom: 'offre', id: 'OFF-2026-0151', onglet: 'redaction' }, false) }
export const EnValidation: Story = { name: '6. En attente de validation — offre « Chargé·e de recrutement »', render: story({ nom: 'offre', id: 'OFF-2026-0148', onglet: 'redaction' }, true) }
export const APublier: Story = { name: '7. Préparer et publier — offre « Chef·fe de projet numérique »', render: story({ nom: 'offre', id: 'OFF-2026-0145', onglet: 'publication' }, true) }
export const Suivi: Story = { name: '8. Suivi — offre publiée « Assistant·e administratif·ve »', render: story({ nom: 'offre', id: 'OFF-2026-0118' }) }
export const Parametres: Story = { name: '9. Paramètres de l\'organisme', render: story({ nom: 'parametres' }) }
