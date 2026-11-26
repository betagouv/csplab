import type { StoryObj } from '@storybook/vue3-vite'
import CreerOffreDecrite from './CreerOffreDecrite.vue'
import EditeurDescription from './EditeurDescription.vue'

// Variante du formulaire de création d'offre où le formulaire est décrit en données (principe de survey-kit,
// proposé par Lucas), puis affiché par un moteur générique fait avec les composants Csp*. Piste 2 : rien n'est installé.
// Données fictives (extraits repris du proto « Offres sans autorisation (MVP) »). Hypothèses et limites : NOTES.md.
const meta = {
  title: 'Prototypes/Offre survey-kit',
  id: 'prototypes-offre-survey-kit',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Le formulaire de création d\'offre n\'est plus écrit écran par écran : il est décrit dans offre.formulaire.json '
          + '(réponses attendues, parties, étapes, pages, conditions d\'affichage et dépendances), et un moteur l\'affiche avec les Csp*. '
          + '« Éditeur » : on modifie la description, le formulaire suit. « Créer une offre » : le formulaire seul, à comparer à la story '
          + 'Offres sans autorisation (MVP) › 2. Créer une offre. Données fictives.',
      },
    },
  },
}

export default meta
type Story = StoryObj

export const Editeur: Story = {
  name: '1. Éditeur — description à gauche, formulaire à droite',
  render: () => ({ components: { EditeurDescription }, template: '<EditeurDescription />' }),
}

export const Creer: Story = {
  name: '2. Créer une offre — formulaire produit par la description',
  render: () => ({ components: { CreerOffreDecrite }, template: '<CreerOffreDecrite />' }),
}
