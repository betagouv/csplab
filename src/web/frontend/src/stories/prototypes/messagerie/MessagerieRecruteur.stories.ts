import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { SettingsArgs } from './shared/settings'
import RecruiterPanel from './recruteur/RecruiterPanel.vue'
import { DEFAULT_ARGS, SETTINGS_ARG_TYPES } from './shared/settings'

type Args = SettingsArgs & {
  pointDeVue: 'jean-marc' | 'karim'
  largeur: 'livree' | 'maquette'
}

const meta = {
  title: 'Prototypes/Messagerie/Recruteur',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Onglet Messages du panneau de candidature, sur un scénario fictif commun : deux conversations sur trois semaines, trois agents et une candidate. '
          + 'Les contrôles changent la présentation du fil, les indices d’immédiateté, l’ordre, le point de vue et la largeur du panneau. '
          + 'Un message envoyé reste dans la page jusqu’au rechargement de la story.',
      },
    },
  },
  argTypes: {
    ...SETTINGS_ARG_TYPES,
    avancement: { table: { disable: true } },
    delai: { table: { disable: true } },
    pointDeVue: {
      name: 'Point de vue',
      control: { type: 'inline-radio' },
      options: ['jean-marc', 'karim'],
      labels: { 'jean-marc': 'Jean-Marc Chateau, auteur de messages', 'karim': 'Karim Benali, découvre la conversation' },
    },
    largeur: {
      name: 'Largeur du panneau',
      control: { type: 'inline-radio' },
      options: ['livree', 'maquette'],
      labels: { livree: 'Panneau livré', maquette: 'Panneau de la maquette' },
    },
  },
  args: {
    ...DEFAULT_ARGS,
    pointDeVue: 'jean-marc',
    largeur: 'livree',
  },
  render: args => ({
    components: { RecruiterPanel },
    setup: () => ({ args }),
    template: '<RecruiterPanel :settings-args="args" :point-de-vue="args.pointDeVue" :largeur="args.largeur" scenario="principal" />',
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
