import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import { CATEGORIES, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Catégories d’étape',
  decorators: [keepTheme, withLevierOption(CATEGORIES)],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
  globals: { interfaceTheme: 'aucun' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const EnTeteTeinte: Story = { name: 'En-tête de colonne teinté, LEE', parameters: { option: 'en-tete-teinte' } }
