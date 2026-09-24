import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { SettingsArgs } from './shared/settings'
import CandidateSpace from './candidat/CandidateSpace.vue'
import PhoneFrame from './candidat/PhoneFrame.vue'
import RecruiterPanel from './recruteur/RecruiterPanel.vue'
import { DEFAULT_ARGS, SETTINGS_ARG_TYPES } from './shared/settings'

const meta = {
  title: 'Prototypes/Messagerie/Échange structuré',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'La proposition de créneaux devient une demande avec un état et une échéance : la candidate choisit un créneau dans le message, l’équipe voit le choix sans échange de texte.',
      },
    },
  },
  argTypes: {
    ...SETTINGS_ARG_TYPES,
    regleDeCote: { table: { disable: true } },
  },
  args: { ...DEFAULT_ARGS, presentation: 'correspondance', reglages: 'differe' },
} satisfies Meta<SettingsArgs>

export default meta
type Story = StoryObj<typeof meta>

export const Candidate: Story = {
  name: 'Candidate, choix du créneau',
  render: args => ({
    components: { CandidateSpace },
    setup: () => ({ args }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" />',
  }),
}

export const CandidateDemande: Story = {
  name: 'Candidate, ouverte sur la demande',
  render: args => ({
    components: { CandidateSpace },
    setup: () => ({ args }),
    template: '<CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" />',
  }),
}

export const CandidateTelephone: Story = {
  name: 'Candidate sur téléphone',
  render: args => ({
    components: { CandidateSpace, PhoneFrame },
    setup: () => ({ args }),
    template: '<PhoneFrame><CandidateSpace :settings-args="args" scenario="creneau-en-attente" ouverture="demande" /></PhoneFrame>',
  }),
}

export const RecruteurEnAttente: Story = {
  name: 'Recruteur, choix attendu',
  render: args => ({
    components: { RecruiterPanel },
    setup: () => ({ args }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-en-attente" />',
  }),
}

export const RecruteurCreneauRetenu: Story = {
  name: 'Recruteur, créneau retenu',
  render: args => ({
    components: { RecruiterPanel },
    setup: () => ({ args }),
    template: '<RecruiterPanel :settings-args="args" point-de-vue="jean-marc" largeur="livree" scenario="creneau-retenu" />',
  }),
}
