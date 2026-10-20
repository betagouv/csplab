import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import LeviersPlanche from '../LeviersPlanche.vue'
import { withLevierOption } from '../options'
import { ONGLETS_DSFR } from './onglets-dsfr'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Leviers/Chrome/Onglets du DSFR',
  decorators: [keepTheme, withLevierOption(ONGLETS_DSFR)],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {
  render: () => ({
    components: { LeviersPlanche },
    setup: () => ({ ONGLETS_DSFR }),
    template: '<LeviersPlanche :options="ONGLETS_DSFR" story-prefix="prototypes-leviers-chrome-onglets-du-dsfr" :largeur="1280" :hauteur="800" />',
  }),
}

const PANNEAU = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}` }
const INTROUVABLE = { appRoute: `${RECRUTEMENT_PATH}/candidatures/d0000000-0000-4000-8000-0000000009ff` }
const LISTE = { appRoute: `${RECRUTEMENT_PATH}/liste` }
const PARAMETRES = { appRoute: ORGANISME_PATH }
const RECRUTEMENTS = { appRoute: `${ORGANISME_PATH}/recrutements` }
const SANS_ONGLETS = { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` }
const TELEPHONE = { viewport: { value: 'mobile1', isRotated: false } }

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...PANNEAU } }
export const KitListe: Story = { name: 'Kit actuel, liste', parameters: { option: 'kit', ...LISTE } }
export const KitRecrutements: Story = { name: 'Kit actuel, liste des recrutements', parameters: { option: 'kit', ...RECRUTEMENTS } }
export const KitParametres: Story = { name: 'Kit actuel, paramètres de l’organisme', parameters: { option: 'kit', ...PARAMETRES } }
export const KitSansOnglets: Story = { name: 'Kit actuel, page sans onglets', parameters: { option: 'kit', ...SANS_ONGLETS } }
export const KitTelephone: Story = { name: 'Kit actuel, téléphone', parameters: { option: 'kit' }, globals: TELEPHONE }

export const CadreFondBlanc: Story = { name: 'Cadre sur fond blanc', parameters: { option: 'cadre-fond-blanc' } }
export const CadreFondBlancPanneau: Story = { name: 'Cadre sur fond blanc, panneau', parameters: { option: 'cadre-fond-blanc', ...PANNEAU } }
export const CadreFondBlancPanneauIntrouvable: Story = { name: 'Cadre sur fond blanc, candidature introuvable', parameters: { option: 'cadre-fond-blanc', ...INTROUVABLE } }
export const CadreFondBlancListe: Story = { name: 'Cadre sur fond blanc, liste', parameters: { option: 'cadre-fond-blanc', ...LISTE } }
export const CadreFondBlancRecrutements: Story = { name: 'Cadre sur fond blanc, liste des recrutements', parameters: { option: 'cadre-fond-blanc', ...RECRUTEMENTS } }
export const CadreFondBlancParametres: Story = { name: 'Cadre sur fond blanc, paramètres de l’organisme', parameters: { option: 'cadre-fond-blanc', ...PARAMETRES } }
export const CadreFondBlancSansOnglets: Story = { name: 'Cadre sur fond blanc, page sans onglets', parameters: { option: 'cadre-fond-blanc', ...SANS_ONGLETS } }
export const CadreFondBlancTelephone: Story = { name: 'Cadre sur fond blanc, téléphone', parameters: { option: 'cadre-fond-blanc' }, globals: TELEPHONE }

export const FiletContenu: Story = { name: 'Filet le long du contenu', parameters: { option: 'filet-contenu' } }
export const FiletContenuPanneau: Story = { name: 'Filet le long du contenu, panneau', parameters: { option: 'filet-contenu', ...PANNEAU } }
export const FiletContenuListe: Story = { name: 'Filet le long du contenu, liste', parameters: { option: 'filet-contenu', ...LISTE } }
export const FiletContenuRecrutements: Story = { name: 'Filet le long du contenu, liste des recrutements', parameters: { option: 'filet-contenu', ...RECRUTEMENTS } }
export const FiletContenuParametres: Story = { name: 'Filet le long du contenu, paramètres de l’organisme', parameters: { option: 'filet-contenu', ...PARAMETRES } }
export const FiletContenuSansOnglets: Story = { name: 'Filet le long du contenu, page sans onglets', parameters: { option: 'filet-contenu', ...SANS_ONGLETS } }
export const FiletContenuTelephone: Story = { name: 'Filet le long du contenu, téléphone', parameters: { option: 'filet-contenu' }, globals: TELEPHONE }

export const CadreFondGris: Story = { name: 'Cadre blanc sur fond gris', parameters: { option: 'cadre-fond-gris' } }
export const CadreFondGrisPanneau: Story = { name: 'Cadre blanc sur fond gris, panneau', parameters: { option: 'cadre-fond-gris', ...PANNEAU } }
export const CadreFondGrisListe: Story = { name: 'Cadre blanc sur fond gris, liste', parameters: { option: 'cadre-fond-gris', ...LISTE } }
export const CadreFondGrisRecrutements: Story = { name: 'Cadre blanc sur fond gris, liste des recrutements', parameters: { option: 'cadre-fond-gris', ...RECRUTEMENTS } }
export const CadreFondGrisParametres: Story = { name: 'Cadre blanc sur fond gris, paramètres de l’organisme', parameters: { option: 'cadre-fond-gris', ...PARAMETRES } }
export const CadreFondGrisSansOnglets: Story = { name: 'Cadre blanc sur fond gris, page sans onglets', parameters: { option: 'cadre-fond-gris', ...SANS_ONGLETS } }
export const CadreFondGrisTelephone: Story = { name: 'Cadre blanc sur fond gris, téléphone', parameters: { option: 'cadre-fond-gris' }, globals: TELEPHONE }
