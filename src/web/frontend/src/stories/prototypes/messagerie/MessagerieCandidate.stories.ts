import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { SettingsArgs } from './shared/settings'
import CandidateSpace from './candidat/CandidateSpace.vue'
import { DEFAULT_ARGS, SETTINGS_ARG_TYPES } from './shared/settings'

type Args = SettingsArgs & {
  ouverture: 'haut' | 'dernier-message'
}

const meta = {
  title: 'Prototypes/Messagerie/Candidate',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Page de la candidature dans l’espace candidat, avec les mêmes conversations vues par Camille Dupont. '
          + 'L’avancement affiche l’étape en cours et la suivante ; la ligne d’attente et la mention sous chaque message envoyé disent ce qui est reçu et ce qui est attendu.',
      },
    },
  },
  argTypes: {
    ...SETTINGS_ARG_TYPES,
    regleDeCote: { table: { disable: true } },
    ouverture: {
      name: 'Ouverture de la page',
      control: { type: 'inline-radio' },
      options: ['haut', 'dernier-message'],
      labels: { 'haut': 'En haut', 'dernier-message': 'Sur le dernier message' },
    },
  },
  args: { ...DEFAULT_ARGS, ouverture: 'haut' },
  render: args => ({
    components: { CandidateSpace },
    setup: () => ({ args }),
    template: '<CandidateSpace :settings-args="args" :ouverture="args.ouverture" scenario="principal" />',
  }),
} satisfies Meta<Args>

export default meta
type Story = StoryObj<typeof meta>

export const Bulles: Story = {
  args: { presentation: 'bulles', reglages: 'immediat' },
}

export const Pile: Story = {
  name: 'Pile de messages',
  args: { presentation: 'pile', reglages: 'immediat' },
}

export const Correspondance: Story = {
  args: { presentation: 'correspondance', reglages: 'differe' },
}

export const BullesDernierMessage: Story = {
  name: 'Bulles, ouverte sur le dernier message',
  args: { presentation: 'bulles', reglages: 'immediat', ouverture: 'dernier-message' },
}

export const CorrespondanceDernierMessage: Story = {
  name: 'Correspondance, ouverte sur le dernier message',
  args: { presentation: 'correspondance', reglages: 'differe', ouverture: 'dernier-message' },
}
