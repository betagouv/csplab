import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import type { CadragePlancheEcran } from '../../leviers/CadragePlanche.vue'
import DeckInterface from '../../DeckInterface.vue'
import { keepTheme } from '../../keepTheme'
import CadrageGrille from '../../leviers/CadrageGrille.vue'
import CadragePlanche from '../../leviers/CadragePlanche.vue'
import MouvementPlanche from '../../leviers/mouvement/MouvementPlanche.vue'
import { regleDuTheme } from '../../leviers/mouvement/theme'
import { cadreDe, CHAMP_DU_DIALOGUE } from '../../leviers/rayons/imbrications'

// Plates of the greige theme for a slide of 1440 x 810, where the story takes about 1280 x 720: the whole screen, then
// what sets the theme apart, enlarged, and on other screens
const meta = {
  title: 'Prototypes/Thèmes/Greige/Planches',
  id: 'prototypes-themes-greige',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'greige' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const ECRANS = 'prototypes-themes-greige-ecrans'
const SOMBRE = { theme: 'dark' }

// A whole screen of 1440 x 810, the proportions of the plate, or a part of a 1440 x 900 screen; a frame leaves out the
// scrollbars that some browsers draw over the lists
function ecran(story: string, cadre: DeckInterfaceCadre = { x: 0, y: 0, width: 1440, height: 810 }): Story {
  const hauteur = cadre.height === 810 ? 810 : 900
  return {
    render: () => ({
      components: { DeckInterface },
      setup: () => ({ ecran: `${ECRANS}--${story}`, cadre, hauteur }),
      template: '<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="hauteur" :cadre="cadre" />',
    }),
  }
}

function planche(colonnes: string[], rangees: { legende?: string, ecrans: CadragePlancheEcran[] }[], echelle: number, taille?: { largeur: number, hauteur: number }): Story {
  return {
    render: () => ({
      components: { CadragePlanche },
      setup: () => ({ colonnes, rangees, echelle, ...taille }),
      template: '<CadragePlanche :colonnes="colonnes" :rangees="rangees" :echelle="echelle" :largeur="largeur" :hauteur="hauteur" />',
    }),
  }
}

export const Ecran: Story = { ...ecran('panneau'), name: 'Kanban et panneau' }
export const EcranSombre: Story = { ...ecran('panneau-sombre'), name: 'Kanban et panneau, sombre', globals: SOMBRE }

// End of the page header over its tabs, end of the panel header over its tabs, top of an empty state
const BANDES = [
  { legende: 'En-tête de page', story: 'kanban', cadre: { x: 1080, y: 40, width: 360, height: 110 } },
  { legende: 'En-tête du panneau', story: 'panneau-vide', cadre: { x: 1080, y: 25, width: 360, height: 110 } },
  { legende: 'État vide', story: 'panneau-vide', cadre: { x: 828, y: 190, width: 360, height: 110 } },
]
export const Trame: Story = {
  ...planche(
    ['Clair', 'Sombre'],
    BANDES.map(({ legende, story, cadre }) => ({
      legende,
      ecrans: [{ story: `${ECRANS}--${story}`, cadre }, { story: `${ECRANS}--${story}-sombre`, cadre }],
    })),
    1.45,
  ),
  name: 'Trame de points',
}

// The sidebar, the view switch, the count of candidatures and the first card of the first column
const COIN = { x: 136, y: 200, width: 476, height: 280 }
export const Gris: Story = {
  ...planche(
    ['Aujourd’hui', 'Greige'],
    [
      { legende: 'Clair', ecrans: [{ story: `${ECRANS}--kit-kanban`, cadre: COIN }, { story: `${ECRANS}--kanban`, cadre: COIN }] },
      { legende: 'Sombre', ecrans: [{ story: `${ECRANS}--kit-kanban-sombre`, cadre: COIN }, { story: `${ECRANS}--kanban-sombre`, cadre: COIN }] },
    ],
    1,
  ),
  name: 'Gris réchauffé',
}

export const Rayons: Story = {
  ...planche(
    ['Carte dans une colonne', 'Boutons et case dans une carte', 'Élément d’un menu ouvert', 'Champ dans un dialogue'],
    [
      { legende: 'Clair', ecrans: [0, 1, 2].map(index => ({ story: `${ECRANS}--imbrications`, cadre: cadreDe(index) })).concat({ story: `${ECRANS}--dialogue`, cadre: CHAMP_DU_DIALOGUE }) },
      { legende: 'Sombre', ecrans: [0, 1, 2].map(index => ({ story: `${ECRANS}--imbrications-sombre`, cadre: cadreDe(index) })).concat({ story: `${ECRANS}--dialogue-sombre`, cadre: CHAMP_DU_DIALOGUE }) },
    ],
    1.5,
  ),
}

// The five states of the card, in their grid at the centre of the screen
const ETATS_DE_LA_CARTE = { x: 230, y: 268, width: 980, height: 364 }
export const Carte: Story = {
  render: () => ({
    components: { CadrageGrille },
    setup: () => ({
      ecrans: [{ story: `${ECRANS}--carte`, legende: 'Clair' }, { story: `${ECRANS}--carte-sombre`, legende: 'Sombre' }],
      cadre: ETATS_DE_LA_CARTE,
    }),
    template: '<CadrageGrille :ecrans="ecrans" :cadre="cadre" :echelle="0.8" :colonnes="1" />',
  }),
  name: 'États de la carte',
}

export const Mouvement: Story = {
  render: () => ({
    components: { MouvementPlanche },
    setup: () => ({ regle: regleDuTheme('greige', 'Greige'), ecran: `${ECRANS}--scene` }),
    template: '<MouvementPlanche :regle="regle" :ecran="ecran" interface-theme="greige" />',
  }),
}

export const Composants: Story = ecran('composants')
export const ComposantsSombre: Story = { ...ecran('composants-sombre'), name: 'Composants, sombre', globals: SOMBRE }

export const Liste: Story = ecran('liste')
export const Parametres: Story = { ...ecran('parametres'), name: 'Paramètres de l’organisme' }
export const Dialogue: Story = ecran('dialogue')
export const Menu: Story = { ...ecran('menu'), name: 'Menu ouvert' }
export const Notification: Story = ecran('notification')
export const EtatsVides: Story = { ...ecran('etats-vides', { x: 0, y: 0, width: 760, height: 430 }), name: 'États vides' }
export const Chargement: Story = ecran('chargement')

const TELEPHONE = { x: 0, y: 0, width: 375, height: 812 }
export const Telephone: Story = {
  ...planche(
    ['Kanban', 'Panneau', 'Kanban, sombre', 'Panneau, sombre'],
    [{
      ecrans: ['telephone', 'telephone-panneau', 'telephone-sombre', 'telephone-panneau-sombre']
        .map(story => ({ story: `${ECRANS}--${story}`, cadre: TELEPHONE })),
    }],
    0.78,
    { largeur: 375, hauteur: 812 },
  ),
  name: 'Téléphone',
}
