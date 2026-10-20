import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import LeviersPlanche from '../LeviersPlanche.vue'
import { withLevierOption } from '../options'
import { SURFACE_CONTENU } from './surface-contenu'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Leviers/Chrome/Contenu posé sur la page',
  decorators: [keepTheme, withLevierOption(SURFACE_CONTENU)],
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
    setup: () => ({ SURFACE_CONTENU }),
    template: '<LeviersPlanche :options="SURFACE_CONTENU" story-prefix="prototypes-leviers-chrome-contenu-posé-sur-la-page" :largeur="1440" :hauteur="900" />',
  }),
}

const panneau = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}` }
const liste = { appRoute: `${RECRUTEMENT_PATH}/liste` }
const parametres = { appRoute: ORGANISME_PATH }
const sansOnglets = { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` }
const telephone = { viewport: { value: 'mobile1', isRotated: false } }

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...panneau } }
export const KitListe: Story = { name: 'Kit actuel, liste', parameters: { option: 'kit', ...liste } }
export const KitParametres: Story = { name: 'Kit actuel, paramètres de l’organisme', parameters: { option: 'kit', ...parametres } }
export const KitSansOnglets: Story = { name: 'Kit actuel, page sans onglets', parameters: { option: 'kit', ...sansOnglets } }
export const KitTelephone: Story = { name: 'Kit actuel, téléphone', parameters: { option: 'kit' }, globals: telephone }

export const OngletOuvert: Story = { name: 'Surface ouverte par l’onglet', parameters: { option: 'onglet-ouvert' } }
export const OngletOuvertPanneau: Story = {
  name: 'Surface ouverte par l’onglet, panneau',
  parameters: { option: 'onglet-ouvert', ...panneau },
}
export const OngletOuvertListe: Story = {
  name: 'Surface ouverte par l’onglet, liste',
  parameters: { option: 'onglet-ouvert', ...liste },
}
export const OngletOuvertParametres: Story = {
  name: 'Surface ouverte par l’onglet, paramètres de l’organisme',
  parameters: { option: 'onglet-ouvert', ...parametres },
}
export const OngletOuvertSansOnglets: Story = {
  name: 'Surface ouverte par l’onglet, page sans onglets',
  parameters: { option: 'onglet-ouvert', ...sansOnglets },
}
export const OngletOuvertTelephone: Story = {
  name: 'Surface ouverte par l’onglet, téléphone',
  parameters: { option: 'onglet-ouvert' },
  globals: telephone,
}

export const ColonneSurface: Story = { name: 'Colonne principale en surface', parameters: { option: 'colonne-surface' } }
export const ColonneSurfacePanneau: Story = {
  name: 'Colonne principale en surface, panneau',
  parameters: { option: 'colonne-surface', ...panneau },
}
export const ColonneSurfaceListe: Story = {
  name: 'Colonne principale en surface, liste',
  parameters: { option: 'colonne-surface', ...liste },
}
export const ColonneSurfaceParametres: Story = {
  name: 'Colonne principale en surface, paramètres de l’organisme',
  parameters: { option: 'colonne-surface', ...parametres },
}
export const ColonneSurfaceSansOnglets: Story = {
  name: 'Colonne principale en surface, page sans onglets',
  parameters: { option: 'colonne-surface', ...sansOnglets },
}
export const ColonneSurfaceTelephone: Story = {
  name: 'Colonne principale en surface, téléphone',
  parameters: { option: 'colonne-surface' },
  globals: telephone,
}
