import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { keepTheme } from '../keepTheme'
import MessagesPlanche from './MessagesPlanche.vue'
import { HABILLAGES, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Habillages, états vides',
  decorators: [keepTheme, withLevierOption(HABILLAGES)],
  parameters: {
    layout: 'fullscreen',
  },
  globals: { interfaceTheme: 'aucun' },
  render: () => ({ components: { MessagesPlanche }, template: '<MessagesPlanche />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const Degrade: Story = { name: 'Dégradé bleu France', parameters: { option: 'degrade' } }
export const Lueur: Story = { name: 'Lueur bleu France et cumulus', parameters: { option: 'lueur' } }
export const Rayures: Story = { name: 'Rayures fines', parameters: { option: 'rayures' } }
export const Points: Story = { name: 'Trame de points', parameters: { option: 'points' } }
export const Grain: Story = { name: 'Grain sur beige gris galet', parameters: { option: 'grain' } }
