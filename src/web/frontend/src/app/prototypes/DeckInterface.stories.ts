import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import DeckInterface from './DeckInterface.vue'
import { keepTheme } from './keepTheme'

const RECRUTEMENT_PATH = `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Deck interface',
  component: DeckInterface,
  decorators: [keepTheme],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
  },
} satisfies Meta<typeof DeckInterface>

export default meta

type Story = StoryObj<typeof meta>

function clair(interfaceTheme: string, density = 'compact') {
  return { interfaceTheme, theme: 'light', density }
}

const APP = { args: { planche: 'ecran' }, render: () => ({ components: { App }, template: '<App />' }) } as const

// The panel opens on its Notes tab: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
const PANNEAU = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}/notes` }

// Kanban screen that the « ecran » plates frame
export const EcranKanban: Story = { ...APP, name: 'Écran, kanban' }

// Sidebar, page header and first columns
const DEBUT_DE_PAGE = { x: 0, y: 0, width: 1024, height: 716 }

// Lever plates of 1280 x 560, centered in the slide
function planche(levier: string, option: string) {
  return { planche: 'ecran', ecran: `prototypes-leviers-${levier}--${option}`, hauteur: 560, cadre: { x: 0, y: 0, width: 1280, height: 560 } } as const
}

export const ArrondisDroits: Story = { name: 'Arrondis, kit actuel', args: planche('arrondis', 'droits'), globals: clair('kit') }
export const ArrondisLegers: Story = { name: 'Arrondis, 2 et 4 px', args: planche('arrondis', 'legers'), globals: clair('kit') }
export const ArrondisMoyens: Story = { name: 'Arrondis, 4 et 8 px', args: planche('arrondis', 'moyens'), globals: clair('kit') }
export const ArrondisMarques: Story = { name: 'Arrondis, 8 et 12 px', args: planche('arrondis', 'marques'), globals: clair('kit') }
export const ArrondisRoles: Story = { name: 'Arrondis, rayons par rôle', args: planche('arrondis', 'roles'), globals: clair('kit') }

const DEBUT = { planche: 'ecran', cadre: DEBUT_DE_PAGE } as const

export const DensiteCompacte: Story = { name: 'Densité compacte', args: DEBUT, globals: clair('kit') }
export const DensiteConfortable: Story = { name: 'Densité confortable', args: DEBUT, globals: clair('kit', 'comfortable') }

export const EcranAujourdhui: Story = { ...APP, name: 'Kanban et panneau, kit', parameters: PANNEAU, globals: clair('kit') }
export const EcranDsfr: Story = { ...APP, name: 'Kanban et panneau, dsfr', parameters: PANNEAU, globals: clair('dsfr') }
export const EcranGreige: Story = { ...APP, name: 'Kanban et panneau, greige', parameters: PANNEAU, globals: clair('greige') }
export const EcranLasuite: Story = { ...APP, name: 'Kanban et panneau, lasuite', parameters: PANNEAU, globals: clair('lasuite') }
