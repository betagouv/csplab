import type { StoryObj } from '@storybook/vue3-vite'
import type { CspLabelItem } from './types'
import { ref } from 'vue'
import { PALETTE_COLOR_NAMES, PALETTE_COLORS } from '@/styles/palette'
import CspLabel from './CspLabel.vue'
import CspLabelList from './CspLabelList.vue'

const meta = {
  title: 'Éléments/Génériques/CspLabel',
  component: CspLabel,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'color', 'size', 'removable', 'removeLabel'],
    },
    docs: {
      description: {
        component: 'Étiquette nommée dont la couleur vient d’une des dix clés de la palette. `CspLabelList` affiche une liste d’étiquettes sur un nombre de lignes limité, suivie de « +N », qui donne les étiquettes masquées dans une infobulle au survol et au focus clavier, et dans une fenêtre contextuelle au clic, au toucher, à Entrée et à Espace. Quand la première étiquette ne tient pas entière à côté de « +N », la liste affiche « +N » seul.',
      },
    },
  },
  argTypes: {
    label: {
      control: { type: 'text' },
      description: 'Texte de l’étiquette.',
      table: { type: { summary: 'string' } },
    },
    color: {
      control: { type: 'select' },
      options: [...PALETTE_COLORS],
      description: 'Clé de couleur de la palette.',
      table: { type: { summary: PALETTE_COLORS.join(' | ') }, defaultValue: { summary: 'grey' } },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md'],
      description: 'Taille : `sm` pour les listes denses, `md` pour les panneaux et les formulaires.',
      table: { type: { summary: 'sm | md' }, defaultValue: { summary: 'sm' } },
    },
    removable: {
      control: { type: 'boolean' },
      description: 'Affiche une croix qui émet `remove`.',
      table: { type: { summary: 'boolean' }, defaultValue: { summary: 'false' } },
    },
    removeLabel: {
      control: { type: 'text' },
      description: 'Nom accessible de la croix, « Retirer l’étiquette {label} » par défaut.',
      table: { type: { summary: 'string' } },
    },
  },
  args: {
    label: 'À relire',
    color: 'blue',
    size: 'sm',
    removable: false,
  },
}

export default meta

type Story = StoryObj<typeof meta>

const LABELS: CspLabelItem[] = [
  { label: 'Prioritaire', color: 'red' },
  { label: 'À relire', color: 'blue' },
  { label: 'Relecture juridique faite', color: 'green' },
  { label: 'Interne', color: 'teal' },
  { label: 'En attente', color: 'yellow' },
  { label: 'Archivé', color: 'grey' },
]

export const Default: Story = {
  name: 'Par défaut',
}

export const Colors: Story = {
  name: 'Couleurs',
  render: () => ({
    components: { CspLabel },
    setup: () => ({ colors: PALETTE_COLORS, names: PALETTE_COLOR_NAMES }),
    template: `
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div v-for="size in ['sm', 'md']" :key="size" style="display: flex; flex-wrap: wrap; gap: 0.25rem;">
          <CspLabel v-for="color in colors" :key="color" :label="names[color]" :color="color" :size="size" />
        </div>
      </div>
    `,
  }),
}

export const Removable: Story = {
  name: 'Retirable',
  render: () => ({
    components: { CspLabelList },
    setup: () => {
      const labels = ref([...LABELS])
      return {
        labels,
        remove: (item: CspLabelItem) => {
          labels.value = labels.value.filter(({ label }) => label !== item.label)
        },
      }
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 1rem; max-width: 24rem;">
        <CspLabelList :labels="labels" removable @remove="remove" />
        <CspLabelList :labels="labels" size="md" removable @remove="remove" />
      </div>
    `,
  }),
}

export const LimitedLines: Story = {
  name: 'Lignes limitées',
  render: () => ({
    components: { CspLabelList },
    setup: () => ({ labels: LABELS }),
    template: `
      <div style="display: flex; flex-direction: column; gap: 1.5rem; width: 15rem;">
        <CspLabelList :labels="labels" :max-lines="2" />
        <CspLabelList :labels="labels" :max-lines="1" />
      </div>
    `,
  }),
}
