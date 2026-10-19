import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import { keepTheme } from '../keepTheme'
import LeviersDetail from './LeviersDetail.vue'
import LeviersPlanche from './LeviersPlanche.vue'
import { ARRONDIS, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Arrondis',
  decorators: [keepTheme, withLevierOption(ARRONDIS)],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { LeviersDetail }, template: '<LeviersDetail variante="arrondis" />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {
  render: () => ({
    components: { LeviersPlanche },
    setup: () => ({ ARRONDIS }),
    template: '<LeviersPlanche :options="ARRONDIS" story-prefix="prototypes-leviers-arrondis" :largeur="1280" :hauteur="560" />',
  }),
}

export const Droits: Story = { name: '0 et 4 px, kit actuel', parameters: { option: 'droits' } }
export const Legers: Story = { name: '2 et 4 px', parameters: { option: 'legers' } }
export const Moyens: Story = { name: '4 et 8 px', parameters: { option: 'moyens' } }
export const Marques: Story = { name: '8 et 12 px', parameters: { option: 'marques' } }
export const RolesLee: Story = { name: 'Rayons par rôle de LEE', parameters: { option: 'roles-lee' } }
