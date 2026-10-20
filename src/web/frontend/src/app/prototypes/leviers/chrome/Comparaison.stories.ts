import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { LevierOption } from '../options'
import { keepTheme } from '../../keepTheme'
import CadrageGrille from '../CadrageGrille.vue'
import { ONGLETS_ALIGNES } from './onglets-alignes'
import { SANS_FILET } from './sans-filet'

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
  ecran('sans-filet', SANS_FILET, 'sans-filet'),
]

// Top left corner of the kanban, in a 1280 x 800 window: the edge of the sidebar, the title row and the line under the
// page header, the tabs, the toolbar and the top of the first column. Three parts enlarged 1.35 times fill a 1280 x 720
// slide
const COIN_DU_KANBAN = { x: 243, y: 60, width: 290, height: 380 }

const coin: Story = {
  render: () => ({
    components: { CadrageGrille },
    setup: () => ({ ECRANS, COIN_DU_KANBAN }),
    template: `<CadrageGrille
      :ecrans="ECRANS"
      :cadre="COIN_DU_KANBAN"
      :echelle="1.35"
      :colonnes="3"
      :largeur="1280"
      :hauteur="800"
    />`,
  }),
}

export const CoinDuKanban: Story = { ...coin, name: 'Coin du kanban' }
export const CoinDuKanbanSombre: Story = { ...coin, name: 'Coin du kanban, sombre', globals: { theme: 'dark' } }
