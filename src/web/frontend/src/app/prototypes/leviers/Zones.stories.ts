import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import LeviersPlanche from './LeviersPlanche.vue'
import { withLevierOption, ZONES } from './options'

const meta = {
  title: 'Prototypes/Leviers/Zones',
  decorators: [keepTheme, withLevierOption(ZONES)],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {
  render: () => ({
    components: { LeviersPlanche },
    setup: () => ({ ZONES }),
    template: '<LeviersPlanche :options="ZONES" story-prefix="prototypes-leviers-zones" :largeur="1280" :hauteur="800" />',
  }),
}

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const GrisDsfr: Story = { name: 'Gris du DSFR', parameters: { option: 'gris-dsfr' } }
export const GrisChauds: Story = { name: 'Gris à peine chauds', parameters: { option: 'gris-chauds' } }
export const CadreBlanc: Story = { name: 'Cadre blanc', parameters: { option: 'cadre-blanc' } }
