import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../keepTheme'
import { HABILLAGES, withLevierOption } from './options'

const meta = {
  title: 'Prototypes/Leviers/Habillages',
  decorators: [keepTheme, withLevierOption(HABILLAGES)],
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

const KANBAN = { appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}` }

export const Kit: Story = { name: 'Kit actuel', parameters: { option: 'kit' } }
export const Degrade: Story = { name: 'Dégradé bleu France', parameters: { option: 'degrade' } }
export const Lueur: Story = { name: 'Lueur bleu France et cumulus', parameters: { option: 'lueur' } }
export const Points: Story = { name: 'Trame de points', parameters: { option: 'points' } }
export const Rayures: Story = { name: 'Rayures fines', parameters: { option: 'rayures' } }
export const Grain: Story = { name: 'Grain sur beige gris galet', parameters: { option: 'grain' } }
export const KitKanban: Story = { name: 'Kit actuel, kanban', parameters: { option: 'kit', ...KANBAN } }
export const DegradeKanban: Story = { name: 'Dégradé bleu France, kanban', parameters: { option: 'degrade', ...KANBAN } }
export const LueurKanban: Story = { name: 'Lueur bleu France et cumulus, kanban', parameters: { option: 'lueur', ...KANBAN } }
export const PointsKanban: Story = { name: 'Trame de points, kanban', parameters: { option: 'points', ...KANBAN } }
export const RayuresKanban: Story = { name: 'Rayures fines, kanban', parameters: { option: 'rayures', ...KANBAN } }
export const GrainKanban: Story = { name: 'Grain sur beige gris galet, kanban', parameters: { option: 'grain', ...KANBAN } }
