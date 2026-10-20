import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import type { CadragePlancheEcran } from '../../leviers/CadragePlanche.vue'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import DeckInterface from '../../DeckInterface.vue'
import { keepTheme } from '../../keepTheme'
import CadragePlanche from '../../leviers/CadragePlanche.vue'
import EtatsVidesPlanche from '../../leviers/fonds/EtatsVidesPlanche.vue'
import { CHARGEMENT, DIALOGUE, MENU, NOTIFICATION } from '../../leviers/rayons/ecrans'
import CartesPlanche from './CartesPlanche.vue'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`
const PANNEAU_PATH = `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}`
// First candidature of the demo, whose notes are empty
const SANS_NOTE_PATH = `${RECRUTEMENT_PATH}/candidatures/d0000000-0000-4000-8000-000000000001/notes`

const meta = {
  title: 'Prototypes/Thèmes/DSFR',
  id: 'prototypes-themes-dsfr',
  decorators: [keepTheme],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
    viewport: {
      options: { telephone: { name: 'Téléphone, 375 px', styles: { width: '375px', height: '812px' }, type: 'mobile' } },
    },
  },
  globals: { interfaceTheme: 'dsfr' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const SOMBRE = { theme: 'dark' }
const TELEPHONE = { viewport: { value: 'telephone', isRotated: false } }

// Screens of the application, that the plates frame. The panel opens on its Notes tab: a sandboxed frame, such as a
// deck slide, blocks the PDF viewer of the CV.
export const EcranKanban: Story = { name: 'Écran, kanban' }
export const EcranPanneau: Story = { name: 'Écran, panneau', parameters: { appRoute: `${PANNEAU_PATH}/notes` } }
export const EcranDocuments: Story = { name: 'Écran, documents', parameters: { appRoute: `${PANNEAU_PATH}/documents` } }
export const EcranMessages: Story = { name: 'Écran, messages', parameters: { appRoute: `${PANNEAU_PATH}/messages` } }
export const EcranSansNote: Story = { name: 'Écran, panneau sans note', parameters: { appRoute: SANS_NOTE_PATH } }
export const EcranListe: Story = { name: 'Écran, liste', parameters: { appRoute: `${RECRUTEMENT_PATH}/liste` } }
export const EcranParametres: Story = { name: 'Écran, paramètres', parameters: { appRoute: ORGANISME_PATH } }
export const EcranMenu: Story = { name: 'Écran, menu ouvert', ...MENU }
export const EcranDialogue: Story = {
  name: 'Écran, dialogue',
  parameters: { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` },
  ...DIALOGUE,
}
export const EcranNotification: Story = { name: 'Écran, notification', ...NOTIFICATION }
export const EcranChargement: Story = { name: 'Écran, chargement', ...CHARGEMENT }
export const EcranEtatsVides: Story = {
  name: 'Écran, états vides',
  render: () => ({ components: { EtatsVidesPlanche }, template: '<EtatsVidesPlanche />' }),
}

// A screen in a window of 1440 x 810, or less high, scaled to the plate
function ecranEntier(ecran: string, hauteur = 810): Story {
  return {
    render: () => ({
      components: { DeckInterface },
      setup: () => ({ ecran: `prototypes-themes-dsfr--${ecran}`, hauteur, cadre: { x: 0, y: 0, width: 1440, height: hauteur } }),
      template: '<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="hauteur" :cadre="cadre" />',
    }),
  }
}

// A part of a screen of 1440 x 900, enlarged to the plate
function partie(ecran: string, cadre: DeckInterfaceCadre): Story {
  return {
    render: () => ({
      components: { DeckInterface },
      setup: () => ({ ecran: `prototypes-themes-dsfr--${ecran}`, cadre }),
      template: '<DeckInterface planche="ecran" :ecran="ecran" :largeur="1440" :hauteur="900" :cadre="cadre" />',
    }),
  }
}

// Parts of several screens side by side
function parties(
  colonnes: string[],
  ecrans: CadragePlancheEcran[],
  echelle: number,
  fenetre = { largeur: 1440, hauteur: 900 },
): Story {
  return {
    render: () => ({
      components: { CadragePlanche },
      setup: () => ({ colonnes, rangees: [{ ecrans }], echelle, fenetre }),
      template: `<CadragePlanche
        :colonnes="colonnes"
        :rangees="rangees"
        :echelle="echelle"
        :largeur="fenetre.largeur"
        :hauteur="fenetre.hauteur"
      />`,
    }),
  }
}

function ecran(nom: string, cadre: DeckInterfaceCadre): CadragePlancheEcran {
  return { story: `prototypes-themes-dsfr--${nom}`, cadre }
}

// Plates of the deck, designed for a window of 1280 x 720 unless their name says otherwise
const kanban = ecranEntier('ecran-kanban')
export const Kanban: Story = kanban
export const KanbanSombre: Story = { ...kanban, name: 'Kanban, sombre', globals: SOMBRE }

const kanbanEtPanneau = ecranEntier('ecran-panneau')
export const KanbanEtPanneau: Story = { ...kanbanEtPanneau, name: 'Kanban et panneau' }
export const KanbanEtPanneauSombre: Story = { ...kanbanEtPanneau, name: 'Kanban et panneau, sombre', globals: SOMBRE }

// Tabs, toolbar and first card of the first two columns, enlarged about twice
const ongletsEtColonnes = partie('ecran-kanban', { x: 257, y: 120, width: 655, height: 368 })
export const OngletsEtColonnes: Story = { ...ongletsEtColonnes, name: 'Onglets et colonnes' }
export const OngletsEtColonnesSombre: Story = { ...ongletsEtColonnes, name: 'Onglets et colonnes, sombre', globals: SOMBRE }

// Designed for a window of 1100 x 620
const cartes: Story = {
  parameters: { appRoute: `${PANNEAU_PATH}/notes` },
  render: () => ({ components: { CartesPlanche }, template: '<CartesPlanche />' }),
}
export const Cartes: Story = { ...cartes, name: 'États d’une carte' }
export const CartesSombre: Story = { ...cartes, name: 'États d’une carte, sombre', globals: SOMBRE }

// The panel from its tab row
const PANNEAU_HAUT = { x: 600, y: 120, width: 840, height: 560 }
const panneau = parties(
  ['Documents', 'Messages'],
  [ecran('ecran-documents', PANNEAU_HAUT), ecran('ecran-messages', PANNEAU_HAUT)],
  0.72,
)
export const Panneau: Story = { ...panneau, name: 'Panneau, documents et messages' }
export const PanneauSombre: Story = { ...panneau, name: 'Panneau, documents et messages, sombre', globals: SOMBRE }

const couches = parties(
  ['Menu', 'Dialogue', 'Notification'],
  [
    ecran('ecran-menu', { x: 1000, y: 20, width: 440, height: 190 }),
    ecran('ecran-dialogue', { x: 524, y: 336, width: 392, height: 236 }),
    ecran('ecran-notification', { x: 992, y: 0, width: 448, height: 150 }),
  ],
  0.9,
)
export const Couches: Story = { ...couches, name: 'Menu, dialogue et notification' }
export const CouchesSombre: Story = { ...couches, name: 'Menu, dialogue et notification, sombre', globals: SOMBRE }

const liste = ecranEntier('ecran-liste')
export const Liste: Story = liste
export const ListeSombre: Story = { ...liste, name: 'Liste, sombre', globals: SOMBRE }

// A window that ends under the fourth row of the members table
const parametres = ecranEntier('ecran-parametres', 756)
export const Parametres: Story = { ...parametres, name: 'Paramètres' }

const etatsVides = parties(
  ['Panneau sans note', 'États vides'],
  [
    ecran('ecran-sans-note', { x: 600, y: 120, width: 840, height: 640 }),
    ecran('ecran-etats-vides', { x: 0, y: 0, width: 800, height: 560 }),
  ],
  0.7,
)
export const EtatsVides: Story = { ...etatsVides, name: 'États vides' }

// Designed for a window of 1440 x 810
export const Chargement: Story = CHARGEMENT

const TELEPHONE_FENETRE = { largeur: 375, hauteur: 812 }
const ECRAN_TELEPHONE = { x: 0, y: 0, width: 375, height: 812 }
const telephone = parties(
  ['Kanban', 'Panneau', 'Liste'],
  [
    ecran('ecran-kanban', ECRAN_TELEPHONE),
    ecran('ecran-panneau', ECRAN_TELEPHONE),
    ecran('ecran-liste', ECRAN_TELEPHONE),
  ],
  0.8,
  TELEPHONE_FENETRE,
)
export const Telephone: Story = { ...telephone, name: 'Téléphone' }
export const TelephoneSombre: Story = { ...telephone, name: 'Téléphone, sombre', globals: SOMBRE }

// The screens on a phone, outside the plates
export const EcranTelephone: Story = { name: 'Écran, kanban sur téléphone', globals: TELEPHONE }
