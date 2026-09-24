import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { ColumnSpec } from './comparaison/SideBySide.vue'
import type { SettingsArgs } from './shared/settings'
import type { Presentation } from './shared/types'
import { computed, onBeforeUnmount, onMounted } from 'vue'
import SideBySide from './comparaison/SideBySide.vue'
import { DEFAULT_ARGS, resolveSettings, SETTINGS_ARG_TYPES } from './shared/settings'

type Args = SettingsArgs & {
  pointDeVue: 'jean-marc' | 'karim'
}

const LABELS: Record<Presentation, string> = {
  bulles: 'Bulles',
  pile: 'Pile de messages',
  correspondance: 'Correspondance',
}

const TWO_COLUMNS_HEIGHT = '30.5rem'
const THREE_COLUMNS_HEIGHT = '40rem'

function column(label: string, viewerId: ColumnSpec['viewerId'], args: SettingsArgs, options: Pick<ColumnSpec, 'scenario' | 'conversationId'> = { scenario: 'principal' }): ColumnSpec {
  return { label, viewerId, settings: resolveSettings(args, 'recruteur'), ...options }
}

const meta = {
  title: 'Prototypes/Messagerie/Comparaison',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Des fils côte à côte, sur le même scénario, à la largeur que prend le fil dans le panneau livré sur un écran de 1440 px.',
      },
    },
  },
  argTypes: {
    ...SETTINGS_ARG_TYPES,
    presentation: { table: { disable: true } },
    avancement: { table: { disable: true } },
    delai: { table: { disable: true } },
    pointDeVue: {
      name: 'Point de vue',
      control: { type: 'inline-radio' },
      options: ['jean-marc', 'karim'],
      labels: { 'jean-marc': 'Jean-Marc Chateau, auteur de messages', 'karim': 'Karim Benali, découvre la conversation' },
    },
  },
  args: { ...DEFAULT_ARGS, pointDeVue: 'jean-marc' },
  decorators: [
    () => ({
      setup() {
        onMounted(() => {
          document.documentElement.style.overflow = 'hidden'
        })
        onBeforeUnmount(() => {
          document.documentElement.style.overflow = ''
        })
      },
      template: '<story />',
    }),
  ],
} satisfies Meta<Args>

export default meta
type Story = StoryObj<Args>

export const TroisPresentations: Story = {
  name: 'Trois présentations, même conversation',
  render: args => ({
    components: { SideBySide },
    setup: () => ({
      height: THREE_COLUMNS_HEIGHT,
      columns: computed(() => (['bulles', 'pile', 'correspondance'] as const).map(presentation =>
        column(LABELS[presentation], args.pointDeVue, { ...args, presentation }),
      )),
    }),
    template: '<SideBySide :columns="columns" :height="height" />',
  }),
}

export const CoteDesBulles: Story = {
  name: 'Côté des bulles',
  render: args => ({
    components: { SideBySide },
    setup: () => ({
      height: TWO_COLUMNS_HEIGHT,
      columns: computed(() => [
        column('Équipe à droite, vu par l’auteur', 'jean-marc', { ...args, presentation: 'bulles', regleDeCote: 'equipe' }, { scenario: 'principal', conversationId: 'pieces' }),
        column('Moi à droite, vu par un collègue', 'karim', { ...args, presentation: 'bulles', regleDeCote: 'moi' }, { scenario: 'principal', conversationId: 'pieces' }),
      ]),
    }),
    template: '<SideBySide :columns="columns" :height="height" />',
  }),
  args: { reglages: 'differe' },
}

export const ImmediatOuDiffere: Story = {
  name: 'Immédiat ou différé',
  render: args => ({
    components: { SideBySide },
    setup: () => ({
      height: TWO_COLUMNS_HEIGHT,
      columns: computed(() => [
        column('Immédiat', 'jean-marc', { ...args, presentation: 'bulles', reglages: 'immediat' }),
        column('Différé', 'jean-marc', { ...args, presentation: 'bulles', reglages: 'differe' }),
      ]),
    }),
    template: '<SideBySide :columns="columns" :height="height" />',
  }),
}

export const ChoixDuCreneau: Story = {
  name: 'Choix du créneau, vu par l’équipe',
  render: args => ({
    components: { SideBySide },
    setup: () => ({
      height: TWO_COLUMNS_HEIGHT,
      columns: computed(() => [
        column('Choix attendu', 'jean-marc', { ...args, presentation: 'correspondance' }, { scenario: 'creneau-en-attente' }),
        column('Créneau retenu', 'jean-marc', { ...args, presentation: 'correspondance' }, { scenario: 'creneau-retenu' }),
      ]),
    }),
    template: '<SideBySide :columns="columns" :height="height" />',
  }),
}
