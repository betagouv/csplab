import type { ArgTypes, StoryObj } from '@storybook/vue3-vite'
import type { JeuDonnees, Utilisateur } from './data/espaceMock'
import type { CibleEspace } from './variants/mobile/EspaceCandidatMobile.vue'
import { offreExterne } from './data/candidatMock'
import CandidatureSansCompteMobile from './variants/mobile/CandidatureSansCompteMobile.vue'
import EspaceCandidatMobile from './variants/mobile/EspaceCandidatMobile.vue'
import OffreMobile from './variants/mobile/OffreMobile.vue'
import PageConnexionMobile from './variants/mobile/PageConnexionMobile.vue'
import ParcoursAvecCompteMobile from './variants/mobile/ParcoursAvecCompteMobile.vue'
import ParcoursSansCompteMobile from './variants/mobile/ParcoursSansCompteMobile.vue'

// Refonte mobile-first : deux parcours indépendants (candidater sans compte / suivre avec un
// compte). Le cadre de 26rem simule un écran de mobile sur le canevas Storybook (desktop) ; les
// composants restent nativement responsives au-delà (media queries min-width).
const meta = {
  title: 'Prototypes/Espace candidat mobile',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Refonte mobile-first de l\'espace candidat : parcours 1 (candidater sans compte) et '
          + 'parcours 2 (espace connecté « strict nécessaire » : mes candidatures, détail, '
          + 'conversations avec pièces jointes, retrait, compte). Voir NOTES.md.',
      },
    },
  },
  decorators: [() => ({
    template: `<div style="max-width:26rem;margin:0 auto;min-height:100vh;box-shadow:0 0 0 1px var(--border-default-grey), 0 8px 24px rgb(0 0 0 / 8%);"><story /></div>`,
  })],
}

export default meta
type Story = StoryObj

interface EspaceArgs {
  jeu: JeuDonnees
  methode: Utilisateur['methode']
  simulerEchecEnvoi: boolean
  cible?: CibleEspace
}

const argTypesEspace: Partial<ArgTypes<EspaceArgs>> = {
  jeu: {
    control: 'select',
    options: ['complet', 'sansTerminees', 'vide'],
    description: 'Jeu de candidatures : complet, sans candidature terminée, ou aucune.',
  },
  methode: {
    control: 'select',
    options: ['formulaire', 'franceconnect'],
    description: 'Mode de connexion (change les champs modifiables dans Mon compte).',
  },
  simulerEchecEnvoi: {
    control: 'boolean',
    description: 'Fait échouer le premier envoi de message pour montrer « Réessayer ».',
  },
  cible: { control: false },
}

const argsEspace: EspaceArgs = { jeu: 'complet', methode: 'formulaire', simulerEchecEnvoi: false }

function renderEspace(args: EspaceArgs) {
  return {
    components: { EspaceCandidatMobile },
    setup: () => ({ args }),
    template: `<EspaceCandidatMobile
      :key="JSON.stringify([args.jeu, args.methode, args.simulerEchecEnvoi])"
      :jeu="args.jeu"
      :methode="args.methode"
      :simuler-echec-envoi="args.simulerEchecEnvoi"
      :cible="args.cible"
    />`,
  }
}

// --- Scénarios principaux, cliquables de bout en bout ---

export const ScenarioA: Story = {
  name: '0A. Scénario — Candidater sans compte',
  render: () => ({
    components: { ParcoursSansCompteMobile },
    template: '<ParcoursSansCompteMobile />',
  }),
}

export const ScenarioB: StoryObj<EspaceArgs> = {
  name: '0B. Scénario — Suivre mes candidatures (connexion → espace)',
  args: argsEspace,
  argTypes: argTypesEspace,
  render: args => ({
    components: { ParcoursAvecCompteMobile },
    setup: () => ({ args }),
    template: `<ParcoursAvecCompteMobile
      :key="args.jeu"
      :jeu="args.jeu"
      :simuler-echec-envoi="args.simulerEchecEnvoi"
    />`,
  }),
}

export const ScenarioC: Story = {
  name: '0C. Scénario — Lien « nouveau message » reçu par courriel',
  render: () => ({
    components: { ParcoursAvecCompteMobile },
    setup: () => ({
      cible: {
        ecran: 'conversation',
        candidatureId: 'cand-innovation-numerique',
        conversationId: 'conv-entretien',
      } satisfies CibleEspace,
    }),
    template: `<ParcoursAvecCompteMobile
      :cible="cible"
      message-contexte="Connectez-vous pour lire votre nouveau message."
    />`,
  }),
}

// --- Parcours 1 : écrans isolés ---

export const Offre: Story = {
  name: 'Parcours 1/Offre',
  render: () => ({
    components: { OffreMobile },
    template: '<OffreMobile />',
  }),
}

export const OffreExterneStory: Story = {
  name: 'Parcours 1/Offre (site partenaire)',
  render: () => ({
    components: { OffreMobile },
    setup: () => ({ offreExterne }),
    template: '<OffreMobile :offre="offreExterne" />',
  }),
}

export const CandidatureFlow: Story = {
  name: 'Parcours 1/Formulaire de candidature',
  render: () => ({
    components: { CandidatureSansCompteMobile },
    template: '<CandidatureSansCompteMobile />',
  }),
}

// --- Parcours 2 : écrans isolés ---

export const Connexion: Story = {
  name: 'Parcours 2/Connexion',
  render: () => ({
    components: { PageConnexionMobile },
    template: '<PageConnexionMobile />',
  }),
}

export const MesCandidatures: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Mes candidatures',
  args: argsEspace,
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const MesCandidaturesSansTerminees: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Mes candidatures — aucune terminée',
  args: { ...argsEspace, jeu: 'sansTerminees' },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const MesCandidaturesVide: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Mes candidatures — état vide',
  args: { ...argsEspace, jeu: 'vide' },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const DetailEnCours: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Détail — candidature en cours',
  args: { ...argsEspace, cible: { ecran: 'detail', candidatureId: 'cand-innovation-numerique' } },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const DetailTerminee: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Détail — candidature terminée (retenue)',
  args: { ...argsEspace, cible: { ecran: 'detail', candidatureId: 'cand-occitanie' } },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const Conversation: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Conversation',
  args: {
    ...argsEspace,
    cible: { ecran: 'conversation', candidatureId: 'cand-innovation-numerique', conversationId: 'conv-entretien' },
  },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const ConversationEchecEnvoi: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Conversation — échec d\'envoi puis « Réessayer »',
  args: {
    ...argsEspace,
    simulerEchecEnvoi: true,
    cible: { ecran: 'conversation', candidatureId: 'cand-innovation-numerique', conversationId: 'conv-entretien' },
  },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const CompteFormulaire: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Mon compte — connexion par formulaire',
  args: { ...argsEspace, cible: { ecran: 'compte' } },
  argTypes: argTypesEspace,
  render: renderEspace,
}

export const CompteFranceConnect: StoryObj<EspaceArgs> = {
  name: 'Parcours 2/Mon compte — connexion FranceConnect',
  args: { ...argsEspace, methode: 'franceconnect', cible: { ecran: 'compte' } },
  argTypes: argTypesEspace,
  render: renderEspace,
}
