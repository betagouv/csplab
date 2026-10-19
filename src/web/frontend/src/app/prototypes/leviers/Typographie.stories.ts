import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import { TYPOGRAPHIE, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Typographie',
  decorators: [keepTheme, withLevierOption(TYPOGRAPHIE)],
  parameters: {
    layout: 'fullscreen',
    // The panel opens on its Notes tab: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}/candidatures/${DEMO_CANDIDATURE.uuid}/notes`,
  },
  globals: { interfaceTheme: 'aucun' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const RolesLee: Story = { name: 'Rôles de texte de LEE', parameters: { option: 'roles-lee' } }
