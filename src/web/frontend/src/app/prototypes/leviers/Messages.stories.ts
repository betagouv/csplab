import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { keepTheme } from '../keepTheme'
import MessagesPlanche from './MessagesPlanche.vue'
import { MESSAGES, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/États et messages',
  decorators: [keepTheme, withLevierOption(MESSAGES)],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'aucun' },
  render: () => ({ components: { MessagesPlanche }, template: '<MessagesPlanche />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const CadresLee: Story = { name: 'Cadre du ton et état vide en carte, LEE', parameters: { option: 'cadres-lee' } }
