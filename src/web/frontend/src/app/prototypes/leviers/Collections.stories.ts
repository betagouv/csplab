import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import { COLLECTIONS, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Collections',
  decorators: [keepTheme, withLevierOption(COLLECTIONS)],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}/liste`,
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const TableLee: Story = { name: 'En-têtes en petites capitales et filets doux, LEE', parameters: { option: 'table-lee' } }
