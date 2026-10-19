import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'

const RECRUTEMENT_PATH = `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`
const CANDIDATURE_PATH = `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}`

const meta = {
  title: 'Prototypes/Écrans',
  component: App,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Vues de l’application rendues par ses routes, avec les données de démonstration des dossiers `__mocks__` et le champ de prototype `etiquettes`.',
      },
    },
  },
} satisfies Meta<typeof App>

export default meta

type Story = StoryObj<typeof meta>

export const Kanban: Story = {
  parameters: { appRoute: RECRUTEMENT_PATH },
}

export const KanbanWithPanel: Story = {
  name: 'Kanban, panneau de candidature',
  parameters: { appRoute: CANDIDATURE_PATH },
}

export const PanelNotes: Story = {
  name: 'Panneau, onglet Notes',
  parameters: { appRoute: `${CANDIDATURE_PATH}/notes` },
}

export const List: Story = {
  name: 'Vue liste',
  parameters: { appRoute: `${RECRUTEMENT_PATH}/liste` },
}
