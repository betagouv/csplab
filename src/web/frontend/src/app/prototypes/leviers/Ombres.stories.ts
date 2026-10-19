import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import { keepTheme } from '../keepTheme'
import LeviersDetail from './LeviersDetail.vue'
import LeviersPlanche from './LeviersPlanche.vue'
import { OMBRES, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Ombres',
  decorators: [keepTheme, withLevierOption(OMBRES)],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
  globals: { interfaceTheme: 'aucun' },
  render: () => ({ components: { LeviersDetail }, template: '<LeviersDetail variante="ombres" />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Comparaison: Story = {
  render: () => ({
    components: { LeviersPlanche },
    setup: () => ({ OMBRES }),
    template: '<LeviersPlanche :options="OMBRES" story-prefix="prototypes-leviers-ombres" :largeur="1280" :hauteur="560" />',
  }),
}

export const SansOmbre: Story = { name: 'Sans ombre', parameters: { option: 'sans-ombre' } }
export const KitActuel: Story = { name: 'Kit actuel', parameters: { option: 'kit-actuel' } }
export const Dsfr: Story = { name: 'Ombres du DSFR', parameters: { option: 'dsfr' } }
export const Douces: Story = { name: 'Ombres douces', parameters: { option: 'douces' } }
export const CouchesLee: Story = { name: 'Ombre des couches superposées, LEE', parameters: { option: 'couches-lee' } }
