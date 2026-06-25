import type { StoryObj } from '@storybook/vue3-vite'
import Ajout from './variants/ajout/Ajout.vue'
import Etat from './variants/etat/Etat.vue'
import InteractionActionsEnLigne from './variants/interaction/InteractionActionsEnLigne.vue'
import InteractionMenuContextuel from './variants/interaction/InteractionMenuContextuel.vue'
import Visibilite from './variants/visibilite/Visibilite.vue'

// Une story par variante : chaque option a sa propre iframe (et sa lightbox dans
// le deck nuxt-slides). Titres groupés par notion via le « / » Storybook.
const meta = {
  title: 'Prototypes/Écran Pipeline',
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component:
          'Pistes d\'interaction pour la liste d\'étapes de recrutement. Contrat de domaine : '
          + 'étapes INITIALE / TERMINALE obligatoires (à position fixe), étapes EN_COURS '
          + 'librement réordonnables. Une story par variante, regroupées par sujet.',
      },
    },
  },
}

export default meta
type Story = StoryObj

// --- Interaction de liste ---

export const InteractionActions: Story = {
  name: 'Interaction/Actions en ligne',
  render: () => ({
    components: { InteractionActionsEnLigne },
    template: '<InteractionActionsEnLigne />',
  }),
}

export const InteractionMenu: Story = {
  name: 'Interaction/Menu contextuel',
  render: () => ({
    components: { InteractionMenuContextuel },
    template: '<InteractionMenuContextuel />',
  }),
}

// --- Visibilité candidat ---

export const VisibiliteColonneMiroir: Story = {
  name: 'Visibilité/Colonne miroir',
  render: () => ({
    components: { Visibilite },
    template: '<Visibilite variant="mirror" />',
  }),
}

export const VisibilitePastilleLegende: Story = {
  name: 'Visibilité/Pastille + légende',
  render: () => ({
    components: { Visibilite },
    template: '<Visibilite variant="inline" />',
  }),
}

// --- Ajout d'étape ---

export const AjoutBoutonBas: Story = {
  name: 'Ajout/Bouton en bas',
  render: () => ({
    components: { Ajout },
    template: '<Ajout approach="bottom" />',
  }),
}

export const AjoutMenuContextuel: Story = {
  name: 'Ajout/Menu contextuel',
  render: () => ({
    components: { Ajout },
    template: '<Ajout approach="menu" />',
  }),
}

export const AjoutModaleGuidee: Story = {
  name: 'Ajout/Modale guidée',
  render: () => ({
    components: { Ajout },
    template: '<Ajout approach="naming" />',
  }),
}

// --- Gestion de l'état ---

export const EtatCommitExplicite: Story = {
  name: 'État/Commit explicite',
  render: () => ({
    components: { Etat },
    template: '<Etat model="commit" />',
  }),
}

export const EtatAutoSave: Story = {
  name: 'État/Auto-save',
  render: () => ({
    components: { Etat },
    template: '<Etat model="auto" />',
  }),
}

export const EtatHybride: Story = {
  name: 'État/Hybride par-action',
  render: () => ({
    components: { Etat },
    template: '<Etat model="hybride" />',
  }),
}
