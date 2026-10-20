import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import { keepTheme } from '../../keepTheme'
import CadrageGrille from '../CadrageGrille.vue'
import { RECRUTEMENT_PATH } from './ecrans'
import OmbresBanc from './OmbresBanc.vue'
import OmbresCartes from './OmbresCartes.vue'
import OmbresComparaison from './OmbresComparaison.vue'
import { OMBRES } from './pistes'

const meta = {
  title: 'Prototypes/Leviers/Ombres/Comparaison',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen', appRoute: RECRUTEMENT_PATH },
  globals: { interfaceTheme: 'kit' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const SOMBRE = { theme: 'dark' }

const cartes: Story = {
  render: () => ({
    components: { OmbresComparaison },
    setup: () => ({ OMBRES }),
    template: '<OmbresComparaison :options="OMBRES" />',
  }),
}

export const Cartes: Story = { ...cartes, name: 'Carte du kanban' }
export const CartesSombre: Story = { ...cartes, name: 'Carte du kanban, sombre', globals: SOMBRE }

// Story files of the options, in the order of OMBRES
const FICHIERS = ['kit-actuel', 'a-plat', 'dsfr', 'douces']

function storyId(index: number, ecran: string): string {
  return `prototypes-leviers-ombres-${FICHIERS[index]}--${ecran}`
}

// The screen with its shadows switched in place, so that one can hover and drag a card, open the menu of the job offer
// or a candidature, and compare the options on the open layer
const banc: Story = {
  render: () => ({
    components: { OmbresBanc },
    setup: () => ({ OMBRES, ecran: storyId(0, 'kanban') }),
    template: '<OmbresBanc :options="OMBRES" :ecran="ecran" />',
  }),
}

export const Banc: Story = { ...banc, name: 'Écran à manipuler' }
export const BancSombre: Story = { ...banc, name: 'Écran à manipuler, sombre', globals: SOMBRE }

// Live cards of each option, to hover, focus and drag
const cartesVivantes: Story = {
  render: () => ({
    components: { OmbresCartes },
    setup: () => ({ OMBRES }),
    template: '<OmbresCartes :options="OMBRES" />',
  }),
}

export const CartesVivantes: Story = { ...cartesVivantes, name: 'Cartes à survoler' }
export const CartesVivantesSombre: Story = { ...cartesVivantes, name: 'Cartes à survoler, sombre', globals: SOMBRE }

// The same part of one screen story of each option, in a 1440 x 900 window
function grille(ecran: string, cadre: DeckInterfaceCadre, echelle: number): Story {
  const ecrans = OMBRES.map((option, index) => ({
    story: storyId(index, ecran),
    legende: option.nom,
  }))
  return {
    render: () => ({
      components: { CadrageGrille },
      setup: () => ({ ecrans, cadre, echelle }),
      template: '<CadrageGrille :ecrans="ecrans" :cadre="cadre" :echelle="echelle" :colonnes="2" />',
    }),
  }
}

// Left edge of the panel over the header and the first card of the first kanban column, down to the gap under the
// card; menu of the job offer under its button, with the line under the page header
const BORD_DU_PANNEAU = { x: 288, y: 304, width: 330, height: 180 }
const MENU_DE_L_OFFRE = { x: 1052, y: 40, width: 360, height: 128 }

export const Panneau: Story = { ...grille('panneau', BORD_DU_PANNEAU, 1.4), name: 'Bord du panneau' }
export const PanneauSombre: Story = { ...grille('panneau', BORD_DU_PANNEAU, 1.4), name: 'Bord du panneau, sombre', globals: SOMBRE }
export const Menu: Story = { ...grille('menu', MENU_DE_L_OFFRE, 1.25), name: 'Menu de l’offre' }
export const MenuSombre: Story = { ...grille('menu', MENU_DE_L_OFFRE, 1.25), name: 'Menu de l’offre, sombre', globals: SOMBRE }
