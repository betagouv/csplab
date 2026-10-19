import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import { PARCOURS, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Parcours',
  decorators: [keepTheme, withLevierOption(PARCOURS)],
  parameters: {
    layout: 'fullscreen',
    // The panel opens on its Notes tab: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}/candidatures/${DEMO_CANDIDATURE.uuid}/notes`,
  },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const CarteOuverteLee: Story = { name: 'Carte ouverte teintée, LEE', parameters: { option: 'carte-ouverte-lee' } }
export const CoteACoteLee: Story = { name: 'Panneau à côté du kanban, LEE', parameters: { option: 'cote-a-cote-lee' } }
