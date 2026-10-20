import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { LevierOption } from '../options'
import { keepTheme } from '../../keepTheme'
import CadrageGrille from '../CadrageGrille.vue'
import { ONGLETS_ALIGNES } from './onglets-alignes'
import { ONGLETS_DSFR } from './onglets-dsfr'
import { SANS_FILET } from './sans-filet'
import { SURFACE_CONTENU } from './surface-contenu'

const meta = {
  title: 'Prototypes/Leviers/Chrome/Comparaison',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'kit' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

// Kanban story of each option, the kit first, with the name of the option
function ecran(fichier: string, options: LevierOption[], id: string): { story: string, legende: string } {
  return { story: `prototypes-leviers-chrome-${fichier}--${id}`, legende: options.find(option => option.id === id)!.nom }
}

const ECRANS = [
  ecran('onglets-alignes', ONGLETS_ALIGNES, 'kit'),
  ecran('onglets-alignes', ONGLETS_ALIGNES, 'onglets-alignes'),
  ecran('onglets-du-dsfr', ONGLETS_DSFR, 'cadre-fond-blanc'),
  ecran('onglets-du-dsfr', ONGLETS_DSFR, 'cadre-fond-gris'),
  ecran('onglets-du-dsfr', ONGLETS_DSFR, 'filet-contenu'),
  ecran('contenu-posé-sur-la-page', SURFACE_CONTENU, 'onglet-ouvert'),
  ecran('contenu-posé-sur-la-page', SURFACE_CONTENU, 'colonne-surface'),
  ecran('sans-filet', SANS_FILET, 'sans-filet'),
]

// Top left corner of the kanban, in a 1280 x 800 window: the edge of the sidebar, the title row and the line under the
// page header, the tabs, the toolbar and the top of the first column
const COIN_DU_KANBAN = { x: 243, y: 60, width: 290, height: 298 }

const coin: Story = {
  render: () => ({
    components: { CadrageGrille },
    setup: () => ({ ECRANS, COIN_DU_KANBAN }),
    template: `<CadrageGrille
      :ecrans="ECRANS"
      :cadre="COIN_DU_KANBAN"
      :echelle="1"
      :colonnes="4"
      :largeur="1280"
      :hauteur="800"
    />`,
  }),
}

export const CoinDuKanban: Story = { ...coin, name: 'Coin du kanban' }
export const CoinDuKanbanSombre: Story = { ...coin, name: 'Coin du kanban, sombre', globals: { theme: 'dark' } }
