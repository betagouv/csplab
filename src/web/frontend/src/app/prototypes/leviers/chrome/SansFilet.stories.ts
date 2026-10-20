import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import CspSkeletonSortableList from '@/components/base/CspSkeleton/CspSkeletonSortableList.vue'
import { keepTheme } from '../../keepTheme'
import LeviersPlanche from '../LeviersPlanche.vue'
import { withLevierOption } from '../options'
import { SANS_FILET } from './sans-filet'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Leviers/Chrome/Séparation par l’espace',
  id: 'prototypes-leviers-chrome-sans-filet',
  decorators: [keepTheme, withLevierOption(SANS_FILET)],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
    viewport: {
      options: { telephone: { name: 'Téléphone, 375 px', styles: { width: '375px', height: '812px' }, type: 'mobile' } },
    },
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {
  render: () => ({
    components: { LeviersPlanche },
    setup: () => ({ SANS_FILET }),
    template: '<LeviersPlanche :options="SANS_FILET" story-prefix="prototypes-leviers-chrome-sans-filet" :largeur="1440" :hauteur="900" />',
  }),
}

// The panel opens on its Notes tab: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
const panneau = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}/notes` }
const liste = { appRoute: `${RECRUTEMENT_PATH}/liste` }
const parametres = { appRoute: ORGANISME_PATH }
const sansOnglets = { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` }
const telephone = { viewport: { value: 'telephone', isRotated: false } }

export const Kit: Story = { name: 'Kit actuel, kanban', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...panneau } }
export const KitListe: Story = { name: 'Kit actuel, liste', parameters: { option: 'kit', ...liste } }
export const KitParametres: Story = { name: 'Kit actuel, paramètres de l’organisme', parameters: { option: 'kit', ...parametres } }
export const KitSansOnglets: Story = { name: 'Kit actuel, page sans onglets', parameters: { option: 'kit', ...sansOnglets } }
export const KitTelephone: Story = { name: 'Kit actuel, téléphone', parameters: { option: 'kit' }, globals: telephone }

// Loading placeholders of the kanban and of the steps list, which read the kanban, region and raised variables
const chargement = {
  render: () => ({
    components: { CspSkeletonKanban, CspSkeletonSortableList },
    template: `<div style="display: grid; gap: var(--csp-space-8); padding: var(--csp-space-8)">
      <CspSkeletonKanban :columns="4" :cards="2" />
      <div style="max-width: 38rem"><CspSkeletonSortableList :rows="4" /></div>
    </div>`,
  }),
}

export const KitChargement: Story = { name: 'Kit actuel, chargement', parameters: { option: 'kit' }, ...chargement }

export const SansFilet: Story = { name: 'Séparation par l’espace, kanban', parameters: { option: 'sans-filet' } }
export const SansFiletPanneau: Story = { name: 'Séparation par l’espace, panneau', parameters: { option: 'sans-filet', ...panneau } }
export const SansFiletListe: Story = { name: 'Séparation par l’espace, liste', parameters: { option: 'sans-filet', ...liste } }
export const SansFiletParametres: Story = {
  name: 'Séparation par l’espace, paramètres de l’organisme',
  parameters: { option: 'sans-filet', ...parametres },
}
export const SansFiletSansOnglets: Story = {
  name: 'Séparation par l’espace, page sans onglets',
  parameters: { option: 'sans-filet', ...sansOnglets },
}
export const SansFiletTelephone: Story = {
  name: 'Séparation par l’espace, téléphone',
  parameters: { option: 'sans-filet' },
  globals: telephone,
}
export const SansFiletChargement: Story = {
  name: 'Séparation par l’espace, chargement',
  parameters: { option: 'sans-filet' },
  ...chargement,
}
