import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import LeviersPlanche from '../LeviersPlanche.vue'
import { withLevierOption } from '../options'
import { ONGLETS_ALIGNES } from './onglets-alignes'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Leviers/Chrome/Onglets alignés',
  id: 'prototypes-leviers-chrome-onglets-alignes',
  decorators: [keepTheme, withLevierOption(ONGLETS_ALIGNES)],
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
    setup: () => ({ ONGLETS_ALIGNES }),
    template: '<LeviersPlanche :options="ONGLETS_ALIGNES" story-prefix="prototypes-leviers-chrome-onglets-alignes" :largeur="1280" :hauteur="800" />',
  }),
}

const PANNEAU = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}` }
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

export const OngletsAlignes: Story = { name: 'Onglets alignés', parameters: { option: 'onglets-alignes' } }
export const OngletsAlignesPanneau: Story = { name: 'Onglets alignés, panneau', parameters: { option: 'onglets-alignes', ...PANNEAU } }
export const OngletsAlignesListe: Story = { name: 'Onglets alignés, liste', parameters: { option: 'onglets-alignes', ...LISTE } }
export const OngletsAlignesRecrutements: Story = { name: 'Onglets alignés, liste des recrutements', parameters: { option: 'onglets-alignes', ...RECRUTEMENTS } }
export const OngletsAlignesParametres: Story = { name: 'Onglets alignés, paramètres de l’organisme', parameters: { option: 'onglets-alignes', ...PARAMETRES } }
export const OngletsAlignesSansOnglets: Story = { name: 'Onglets alignés, page sans onglets', parameters: { option: 'onglets-alignes', ...SANS_ONGLETS } }
export const OngletsAlignesTelephone: Story = { name: 'Onglets alignés, téléphone', parameters: { option: 'onglets-alignes' }, globals: TELEPHONE }
