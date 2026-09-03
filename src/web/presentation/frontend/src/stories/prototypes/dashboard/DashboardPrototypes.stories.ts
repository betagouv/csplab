import type { StoryObj } from '@storybook/vue3-vite'
import Disposition from './variants/disposition/Disposition.vue'

// Sujet unique retenu après cadrage : liste priorisée unique (« Nouveaux CV »
// en tête de liste, plus grand que le reste, plutôt que deux blocs séparés).
// Les deux stories principales comparent la disposition des blocs Mes
// recrutements / Mes tâches sous cette liste ; la 3e story montre l'état
// du bloc dominant quand il n'y a plus aucun nouveau CV à traiter.
const meta = {
  title: 'Prototypes/Tableau de bord',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Page d\'accueil de l\'ATS. Navigation complète entre Tableau de bord / Mes '
          + 'recrutements / Mes tâches via le menu latéral. Cliquer un recrutement ou une '
          + 'tâche ouvre sa fiche détail ; cliquer « Nouveaux CV » ou une ligne de la liste '
          + '« À traiter » mène vers la page correspondante.',
      },
    },
  },
}

export default meta
type Story = StoryObj

export const DispositionColonnes: Story = {
  name: 'Disposition/Colonnes côte à côte',
  render: () => ({
    components: { Disposition },
    template: '<Disposition layout="colonnes" />',
  }),
}

export const DispositionEmpilee: Story = {
  name: 'Disposition/Sections empilées',
  render: () => ({
    components: { Disposition },
    template: '<Disposition layout="empile" />',
  }),
}

export const CasLimiteAucunNouveauCV: Story = {
  name: 'Cas limite/Aucun nouveau CV',
  render: () => ({
    components: { Disposition },
    template: '<Disposition layout="colonnes" scenario="calme" />',
  }),
}
