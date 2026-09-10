import type { StoryObj } from '@storybook/vue3-vite'
import PageOffre from './variants/offre/PageOffre.vue'

// Une story par écran/variante, groupées par notion via le « / » Storybook.
// Prototype isolé : pas d'API, pas de router — données mock dans data/candidatMock.ts.
const meta = {
  title: 'Prototypes/Espace candidat',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Parcours candidat côté fonction publique : découverte d\'une offre, candidature '
          + '(avec ou sans compte), confirmation, puis suivi dans un espace connecté. Pensé à '
          + 'part de l\'ATS recruteur, autour des besoins du candidat.',
      },
    },
  },
}

export default meta
type Story = StoryObj

// --- Page offre ---

export const Offre: Story = {
  name: 'Offre/Page offre',
  render: () => ({
    components: { PageOffre },
    template: '<PageOffre />',
  }),
}
