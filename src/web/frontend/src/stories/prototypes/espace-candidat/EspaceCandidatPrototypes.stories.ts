import type { StoryObj } from '@storybook/vue3-vite'
import CandidatureAvecCompte from './variants/candidature/CandidatureAvecCompte.vue'
import CandidatureAvecCv from './variants/candidature/CandidatureAvecCv.vue'
import CandidatureFormulaire from './variants/candidature/CandidatureFormulaire.vue'
import CandidatureUnique from './variants/candidature-unique/CandidatureUnique.vue'
import EspaceCandidatConnecte from './variants/espace/EspaceCandidatConnecte.vue'
import PageOffre from './variants/offre/PageOffre.vue'
import ParcoursCandidatureUnique from './variants/parcours-complet/ParcoursCandidatureUnique.vue'
import ParcoursComplet from './variants/parcours-complet/ParcoursComplet.vue'
import SuccesAvecCompte from './variants/succes/SuccesAvecCompte.vue'
import SuccesSansCompte from './variants/succes/SuccesSansCompte.vue'

// Une story par écran/variante, groupées par notion via le « / » Storybook.
// Prototype isolé : pas d'API, pas de router — données mock dans data/candidatMock.ts.
const meta = {
  title: 'Prototypes/Espace candidat',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Parcours candidat côté fonction publique : découverte d\'une offre, candidature '
          + '(avec ou sans compte), confirmation, puis suivi dans un espace connecté. Pensé à '
          + 'part de l\'ATS recruteur, autour des besoins du candidat.',
      },
    },
  },
}

export default meta
type Story = StoryObj

// --- Scénario principal : le parcours complet, cliquable de bout en bout ---

export const ParcoursPrincipal: Story = {
  name: '0. Scénario principal — modalité unique (cliquable de bout en bout)',
  render: () => ({
    components: { ParcoursCandidatureUnique },
    template: '<ParcoursCandidatureUnique />',
  }),
}

export const ParcoursAvecChoix: Story = {
  name: '0bis. Variante — avec choix du mode de candidature',
  render: () => ({
    components: { ParcoursComplet },
    template: '<ParcoursComplet />',
  }),
}

// --- Page offre (isolée, pour comparer) ---

export const Offre: Story = {
  name: 'Offre/Page offre',
  render: () => ({
    components: { PageOffre },
    template: '<PageOffre />',
  }),
}

// --- Parcours de candidature ---

export const CandidatureCv: Story = {
  name: 'Candidature/Avec un CV',
  render: () => ({
    components: { CandidatureAvecCv },
    template: '<CandidatureAvecCv />',
  }),
}

export const CandidatureCompte: Story = {
  name: 'Candidature/Avec un compte',
  render: () => ({
    components: { CandidatureAvecCompte },
    template: '<CandidatureAvecCompte />',
  }),
}

export const CandidatureFormulaireStory: Story = {
  name: 'Candidature/Avec un formulaire',
  render: () => ({
    components: { CandidatureFormulaire },
    template: '<CandidatureFormulaire />',
  }),
}

export const CandidatureUniqueStory: Story = {
  name: 'Candidature/Modalité unique (formulaire + pop-in de succès)',
  render: () => ({
    components: { CandidatureUnique },
    template: '<CandidatureUnique />',
  }),
}

// --- Écran de succès ---

export const SuccesSansCompteStory: Story = {
  name: 'Succès/Sans compte',
  render: () => ({
    components: { SuccesSansCompte },
    template: '<SuccesSansCompte />',
  }),
}

export const SuccesAvecCompteStory: Story = {
  name: 'Succès/Avec compte',
  render: () => ({
    components: { SuccesAvecCompte },
    template: '<SuccesAvecCompte />',
  }),
}

// --- Espace candidat connecté ---

export const EspaceConnecte: Story = {
  name: 'Espace connecté/Accueil, messages, documents',
  render: () => ({
    components: { EspaceCandidatConnecte },
    template: '<EspaceCandidatConnecte />',
  }),
}
