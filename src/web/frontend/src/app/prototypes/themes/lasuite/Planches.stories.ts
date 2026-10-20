import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import App from '@/app/App.vue'
import DeckInterface from '../../DeckInterface.vue'
import { keepTheme } from '../../keepTheme'
import CadrageGrille from '../../leviers/CadrageGrille.vue'
import MouvementScene from '../../leviers/mouvement/MouvementScene.vue'
import { NOTES, PANNEAU, RECRUTEMENT_PATH } from '../../leviers/rayons/ecrans'
import LasuiteCartes from './LasuiteCartes.vue'
import LasuiteComposants from './LasuiteComposants.vue'
import LasuiteMouvement from './LasuiteMouvement.vue'

// Plates of the theme for a slide of 1440 x 810, where the story takes about 1280 x 720
const meta = {
  title: 'Prototypes/Thèmes/La Suite',
  id: 'prototypes-themes-lasuite',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen', appRoute: RECRUTEMENT_PATH },
  globals: { interfaceTheme: 'lasuite' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const SOMBRE = { interfaceTheme: 'lasuite', theme: 'dark' }
const ECRANS = 'prototypes-themes-lasuite-ecrans'

// The kanban with the panel open on its notes: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
const ecran: Story = { parameters: NOTES, render: () => ({ components: { App }, template: '<App />' }) }

// A part of a screen, enlarged to the plate
function gros(story: string, cadre: DeckInterfaceCadre, ecran = { largeur: 1440, hauteur: 900 }): Story {
  return {
    render: () => ({
      components: { DeckInterface },
      setup: () => ({ ecran: `${ECRANS}--${story}`, cadre, ...ecran }),
      template: '<DeckInterface planche="ecran" :ecran="ecran" :largeur="largeur" :hauteur="hauteur" :cadre="cadre" />',
    }),
  }
}

// Screens side by side, each with a short caption
function grille(ecrans: { story: string, legende: string }[], options: { cadre: DeckInterfaceCadre, echelle: number, colonnes: number, largeur?: number, hauteur?: number }): Story {
  return {
    render: () => ({
      components: { CadrageGrille },
      setup: () => ({ ecrans: ecrans.map(({ story, legende }) => ({ story: `${ECRANS}--${story}`, legende })), options }),
      template: '<CadrageGrille :ecrans="ecrans" v-bind="options" />',
    }),
  }
}

const cartes: Story = {
  parameters: PANNEAU,
  render: () => ({ components: { LasuiteCartes }, template: '<LasuiteCartes />' }),
}
const composants: Story = { render: () => ({ components: { LasuiteComposants }, template: '<LasuiteComposants />' }) }

const TELEPHONE = { x: 0, y: 0, width: 375, height: 812 }
const PAGE = { x: 0, y: 0, width: 1440, height: 810 }

export const Ecran: Story = { ...ecran, name: 'Kanban et panneau' }
export const EcranSombre: Story = { ...ecran, name: 'Kanban et panneau, sombre', globals: SOMBRE }
// A screen of 1024 x 576, where the header and the toolbar hold in the width
const ECRAN_ETROIT = { largeur: 1024, hauteur: 576 }
const ETROIT = { x: 0, y: 0, width: 1024, height: 576 }
// The panel of a screen of 1440 x 485: its header, its tabs, its notes and the buttons of its footer
const ECRAN_BAS = { largeur: 1440, hauteur: 485 }
const PANNEAU_SEUL = { x: 577, y: 0, width: 863, height: 485 }

export const Navigation: Story = { ...gros('kanban', ETROIT, ECRAN_ETROIT), name: 'Navigation et en-tête' }
export const NavigationSombre: Story = {
  ...gros('kanban-sombre', ETROIT, ECRAN_ETROIT),
  name: 'Navigation et en-tête, sombre',
  globals: SOMBRE,
}
export const Panneau: Story = { ...gros('notes', PANNEAU_SEUL, ECRAN_BAS) }
export const PanneauSombre: Story = {
  ...gros('notes-sombre', PANNEAU_SEUL, ECRAN_BAS),
  name: 'Panneau, sombre',
  globals: SOMBRE,
}
export const Cartes: Story = { ...cartes, name: 'États d’une carte' }
export const CartesSombre: Story = { ...cartes, name: 'États d’une carte, sombre', globals: SOMBRE }
export const Composants: Story = { ...composants }
export const ComposantsSombre: Story = { ...composants, name: 'Composants, sombre', globals: SOMBRE }
export const Mouvement: Story = {
  render: () => ({ components: { LasuiteMouvement }, template: '<LasuiteMouvement scene="prototypes-themes-lasuite--scene" />' }),
}
export const Scene: Story = {
  name: 'Mouvement, écran',
  render: () => ({ components: { MouvementScene }, template: '<MouvementScene />' }),
}
export const Telephone: Story = {
  ...grille([
    { story: 'telephone', legende: 'Kanban' },
    { story: 'telephone-panneau', legende: 'Panneau' },
    { story: 'telephone-sombre', legende: 'Kanban, sombre' },
    { story: 'telephone-panneau-sombre', legende: 'Panneau, sombre' },
  ], { cadre: TELEPHONE, echelle: 0.76, colonnes: 4, largeur: 375, hauteur: 812 }),
  name: 'Téléphone',
}
export const AutresEcrans: Story = {
  ...grille([
    { story: 'liste', legende: 'Liste' },
    { story: 'parametres', legende: 'Paramètres' },
    { story: 'dialogue', legende: 'Dialogue' },
    { story: 'notification', legende: 'Notification' },
  ], { cadre: PAGE, echelle: 0.36, colonnes: 2 }),
  name: 'Autres écrans',
}
export const AutresEcransSombre: Story = {
  ...grille([
    { story: 'liste-sombre', legende: 'Liste' },
    { story: 'parametres-sombre', legende: 'Paramètres' },
    { story: 'dialogue-sombre', legende: 'Dialogue' },
    { story: 'notification-sombre', legende: 'Notification' },
  ], { cadre: PAGE, echelle: 0.36, colonnes: 2 }),
  name: 'Autres écrans, sombre',
  globals: SOMBRE,
}
