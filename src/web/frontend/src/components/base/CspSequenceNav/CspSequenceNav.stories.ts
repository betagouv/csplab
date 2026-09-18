import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { computed, ref } from 'vue'
import CspSequenceNav from './CspSequenceNav.vue'

const meta = {
  title: 'Éléments/Génériques/CspSequenceNav',
  component: CspSequenceNav,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Navigation séquentielle entre les éléments d’une liste : boutons Précédent et Suivant, et compteur de position annoncé aux technologies d’assistance. Le composant ne connaît pas la liste : il reçoit la position, le total et l’état de chaque bouton, et émet `previous` et `next`. Le slot par défaut ajoute un contexte au-dessus du compteur.',
      },
    },
  },
  argTypes: {
    position: {
      control: { type: 'number', min: 1 },
      description: 'Position de l’élément courant, à partir de 1. `null` quand la position est inconnue : le compteur est masqué.',
    },
    total: {
      control: { type: 'number', min: 0 },
      description: 'Nombre total d’éléments.',
    },
    itemLabel: {
      control: 'text',
      description: 'Nom de l’élément affiché dans le compteur.',
      table: { defaultValue: { summary: 'Élément' } },
    },
    label: {
      control: 'text',
      description: 'Nom accessible de la navigation.',
      table: { defaultValue: { summary: 'Navigation entre les éléments' } },
    },
    previousDisabled: { control: 'boolean' },
    nextDisabled: { control: 'boolean' },
  },
  args: {
    position: 2,
    total: 4,
    itemLabel: 'Élément',
    previousDisabled: false,
    nextDisabled: false,
  },
} satisfies Meta<typeof CspSequenceNav>

export default meta
type Story = StoryObj<typeof meta>

export const Defaut: Story = {
  name: 'Par défaut',
}

export const PremierElement: Story = {
  name: 'Premier élément',
  args: { position: 1, previousDisabled: true },
}

export const PositionInconnue: Story = {
  name: 'Position inconnue',
  args: { position: null, previousDisabled: true, nextDisabled: true },
}

export const AvecContexte: Story = {
  name: 'Avec un contexte',
  render: args => ({
    components: { CspSequenceNav },
    setup: () => ({ args }),
    template: `
      <CspSequenceNav v-bind="args">
        Dossier : En cours
      </CspSequenceNav>
    `,
  }),
}

export const Interactif: Story = {
  render: () => ({
    components: { CspSequenceNav },
    setup() {
      const total = 5
      const position = ref(1)
      return {
        total,
        position,
        isFirst: computed(() => position.value === 1),
        isLast: computed(() => position.value === total),
      }
    },
    template: `
      <CspSequenceNav
        :position="position"
        :total="total"
        item-label="Page"
        :previous-disabled="isFirst"
        :next-disabled="isLast"
        @previous="position--"
        @next="position++"
      />
    `,
  }),
}
