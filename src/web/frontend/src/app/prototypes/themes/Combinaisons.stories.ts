import type { Meta, StoryObj } from '@storybook/vue3-vite'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import CadrageGrille from '../leviers/CadrageGrille.vue'
import { RECRUTEMENT_PATH } from '../leviers/rayons/ecrans'

// A theme is a background, radii and a density on the root element: the themes side by side, then one theme in its
// three densities, from screens of the application that the plates frame
const meta = {
  title: 'Prototypes/Thèmes/Combinaisons',
  id: 'prototypes-themes-combinaisons',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen', appRoute: RECRUTEMENT_PATH },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const ID = 'prototypes-themes-combinaisons'
// First candidature of the demo, whose notes are empty
const NOTES_VIDES = { appRoute: `${RECRUTEMENT_PATH}/candidatures/d0000000-0000-4000-8000-000000000001/notes` }

export const KanbanKit: Story = { name: 'Kanban, kit', globals: { interfaceTheme: 'kit' } }
export const KanbanDsfr: Story = { name: 'Kanban, DSFR', globals: { interfaceTheme: 'dsfr' } }
export const KanbanGreige: Story = { name: 'Kanban, greige', globals: { interfaceTheme: 'greige' } }
export const KanbanLasuite: Story = { name: 'Kanban, La Suite', globals: { interfaceTheme: 'lasuite' } }
export const PanneauKit: Story = { name: 'Panneau, kit', parameters: NOTES_VIDES, globals: { interfaceTheme: 'kit' } }
export const PanneauDsfr: Story = { name: 'Panneau, DSFR', parameters: NOTES_VIDES, globals: { interfaceTheme: 'dsfr' } }
export const PanneauGreige: Story = { name: 'Panneau, greige', parameters: NOTES_VIDES, globals: { interfaceTheme: 'greige' } }
export const PanneauLasuite: Story = { name: 'Panneau, La Suite', parameters: NOTES_VIDES, globals: { interfaceTheme: 'lasuite' } }
export const KanbanDsfrConfortable: Story = { name: 'Kanban, DSFR, confortable', globals: { interfaceTheme: 'dsfr', density: 'comfortable' } }
export const KanbanDsfrGrande: Story = { name: 'Kanban, DSFR, grande', globals: { interfaceTheme: 'dsfr', density: 'large' } }

// Screens in a grid, a cell per theme or per density
function grille(ecrans: { legende: string, story: string }[], cadre: { x: number, y: number, width: number, height: number }, echelle: number, colonnes: number): Story {
  const cases = ecrans.map(({ legende, story }) => ({ legende, story: `${ID}--${story}` }))
  return {
    render: () => ({
      components: { CadrageGrille },
      setup: () => ({ cases, cadre, echelle, colonnes }),
      template: '<CadrageGrille :ecrans="cases" :cadre="cadre" :echelle="echelle" :colonnes="colonnes" />',
    }),
  }
}

export const Themes: Story = {
  ...grille(
    [
      { legende: 'Aujourd’hui', story: 'panneau-kit' },
      { legende: 'DSFR, dégradé, grain et rayons discrets', story: 'panneau-dsfr' },
      { legende: 'Greige, gris réchauffés, trame et rayons discrets', story: 'panneau-greige' },
      { legende: 'La Suite, couleurs et rayons de son kit', story: 'panneau-lasuite' },
    ],
    { x: 0, y: 0, width: 1440, height: 810 },
    0.4,
    2,
  ),
  name: 'Thèmes côte à côte',
}

// The left part of the kanban, where the navigation, the page header and the cards show the size of the text
export const Densites: Story = {
  ...grille(
    [
      { legende: 'Compacte, texte à 14 px', story: 'kanban-dsfr' },
      { legende: 'Confortable, texte à 16 px', story: 'kanban-dsfr-confortable' },
      { legende: 'Grande, texte à 18 px', story: 'kanban-dsfr-grande' },
    ],
    { x: 0, y: 0, width: 960, height: 900 },
    0.42,
    3,
  ),
  name: 'Densités du thème DSFR',
}
