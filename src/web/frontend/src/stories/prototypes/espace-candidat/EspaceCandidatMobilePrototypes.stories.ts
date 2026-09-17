import type { StoryObj } from '@storybook/vue3-vite'
import { offreExterne } from './data/candidatMock'
import AccueilCandidaturesMobile from './variants/mobile/AccueilCandidaturesMobile.vue'
import CandidatureSansCompteMobile from './variants/mobile/CandidatureSansCompteMobile.vue'
import EspaceCandidatMobile from './variants/mobile/EspaceCandidatMobile.vue'
import OffreMobile from './variants/mobile/OffreMobile.vue'
import PageConnexionMobile from './variants/mobile/PageConnexionMobile.vue'
import ParcoursAvecCompteMobile from './variants/mobile/ParcoursAvecCompteMobile.vue'
import ParcoursSansCompteMobile from './variants/mobile/ParcoursSansCompteMobile.vue'

// Refonte mobile-first : deux parcours indépendants (candidater sans compte / suivre avec
// compte). Composants dans variants/mobile/, fragments communs dans shared/mobile/.
// Le cadre de 390px simule un écran de mobile sur le canevas Storybook (desktop) ; les
// composants restent nativement responsives au-delà (cf. media queries min-width).
const meta = {
  title: 'Prototypes/Espace candidat mobile',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Refonte mobile-first de l\'espace candidat : parcours 1 (candidater sans compte, '
          + 'obligatoire) et parcours 2 (suivre ses candidatures avec un compte, facultatif). '
          + 'Voir aussi « Prototypes/Espace candidat » pour l\'itération desktop précédente.',
      },
    },
  },
  decorators: [() => ({
    template: `<div style="max-width:390px;margin:0 auto;min-height:100vh;box-shadow:0 0 0 1px var(--border-default-grey), 0 8px 24px rgb(0 0 0 / 8%);"><story /></div>`,
  })],
}

export default meta
type Story = StoryObj

// --- Scénarios principaux, cliquables de bout en bout ---

export const ScenarioA: Story = {
  name: '0A. Scénario — Candidater sans compte',
  render: () => ({
    components: { ParcoursSansCompteMobile },
    template: '<ParcoursSansCompteMobile />',
  }),
}

export const ScenarioB: Story = {
  name: '0B. Scénario — Suivre avec un compte',
  render: () => ({
    components: { ParcoursAvecCompteMobile },
    template: '<ParcoursAvecCompteMobile />',
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

export const AccueilEspace: Story = {
  name: 'Parcours 2/Accueil espace candidat',
  render: () => ({
    components: { AccueilCandidaturesMobile },
    template: '<AccueilCandidaturesMobile />',
  }),
}

export const EspaceComplet: Story = {
  name: 'Parcours 2/Espace connecté (avec navigation)',
  render: () => ({
    components: { EspaceCandidatMobile },
    template: '<EspaceCandidatMobile />',
  }),
}
