import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_ORGANISME_AGENT } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'

const SUPERVISEUR_PATH = `/organismes/${DEMO_ORGANISME.uuid}/accueil`
const AGENT_PATH = `/organismes/${DEMO_ORGANISME_AGENT.uuid}/accueil`

const meta = {
  title: 'Prototypes/Page d’accueil',
  component: App,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Deux pistes pour la page d’accueil de l’organisme, en version superviseur et en version agent. Piste 1 : tuiles décrites. Piste 2 : parcours guidé.',
      },
    },
  },
} satisfies Meta<typeof App>

export default meta

type Story = StoryObj<typeof meta>

export const TuilesSuperviseur: Story = {
  name: 'Piste 1, tuiles décrites, superviseur',
  parameters: { appRoute: SUPERVISEUR_PATH },
}

export const TuilesAgent: Story = {
  name: 'Piste 1, tuiles décrites, agent',
  parameters: { appRoute: AGENT_PATH },
}

export const ParcoursSuperviseur: Story = {
  name: 'Piste 2, parcours guidé, superviseur',
  parameters: { appRoute: `${SUPERVISEUR_PATH}?piste=parcours` },
}

export const ParcoursAgent: Story = {
  name: 'Piste 2, parcours guidé, agent',
  parameters: { appRoute: `${AGENT_PATH}?piste=parcours` },
}
