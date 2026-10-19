import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import LeviersPlanche from './LeviersPlanche.vue'
import { CHROME, withLevierOption } from './options'

const RECRUTEMENT_PATH = `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`

const meta = {
  title: 'Prototypes/Leviers/Chrome',
  decorators: [keepTheme, withLevierOption(CHROME)],
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
    setup: () => ({ CHROME }),
    template: '<LeviersPlanche :options="CHROME" story-prefix="prototypes-leviers-chrome" :largeur="1280" :hauteur="800" />',
  }),
}

const withPanel = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}` }

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...withPanel } }
export const TeinteUnifie: Story = { name: 'Chrome teinté unifié', parameters: { option: 'teinte-unifie' } }
export const TeinteUnifiePanneau: Story = { name: 'Chrome teinté unifié, panneau', parameters: { option: 'teinte-unifie', ...withPanel } }
export const ToutBlanc: Story = { name: 'Tout blanc, filets doux', parameters: { option: 'tout-blanc' } }
export const ToutBlancPanneau: Story = { name: 'Tout blanc, filets doux, panneau', parameters: { option: 'tout-blanc', ...withPanel } }
export const Separe: Story = { name: 'Barre latérale teintée, en-tête blanc', parameters: { option: 'separe' } }
export const SeparePanneau: Story = { name: 'Barre latérale teintée, en-tête blanc, panneau', parameters: { option: 'separe', ...withPanel } }
export const BlancBorduresFermes: Story = { name: 'Chrome blanc, bordures fermes', parameters: { option: 'blanc-bordures-fermes' } }
export const BlancBorduresFermesPanneau: Story = {
  name: 'Chrome blanc, bordures fermes, panneau',
  parameters: { option: 'blanc-bordures-fermes', ...withPanel },
}
