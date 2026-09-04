import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'

type CspSegmentedControlProps = ComponentPropsAndSlots<typeof CspSegmentedControl>

const DEFAULT_OPTIONS = [
  { value: 'option-1', label: 'Option 1' },
  { value: 'option-2', label: 'Option 2' },
  { value: 'option-3', label: 'Option 3' },
]

const ICON_OPTIONS = [
  { value: 'grille', label: 'Grille', icon: 'ri:layout-grid-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const meta = {
  title: 'Éléments/Génériques/CspSegmentedControl',
  component: CspSegmentedControl,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'options', 'legend', 'hideLegend', 'inlineLegend', 'size', 'disabled'],
    },
    docs: {
      description: {
        component: 'Contrôle segmenté du DSFR : une option unique parmi deux à cinq, liée via `v-model`. La légende est obligatoire ; `hideLegend` la réserve aux lecteurs d\'écran.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Valeur sélectionnée.',
      table: { type: { summary: 'string' } },
    },
    options: {
      control: { type: 'object' },
      description: 'Options du contrôle.',
      table: { type: { summary: '{ value: string; label: string; icon?: string; disabled?: boolean }[]' } },
    },
    legend: {
      control: { type: 'text' },
      description: 'Légende du groupe, toujours présente pour les technologies d\'assistance.',
    },
    hideLegend: {
      control: { type: 'boolean' },
      description: 'Masque visuellement la légende.',
    },
    inlineLegend: {
      control: { type: 'boolean' },
      description: 'Affiche la légende sur la même ligne que le contrôle.',
    },
    size: {
      control: { type: 'select' },
      options: ['sm', 'md'],
      table: { defaultValue: { summary: 'md' } },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive tout le groupe.',
    },
  },
  args: {
    modelValue: 'option-1',
    options: DEFAULT_OPTIONS,
    legend: 'Choix',
    hideLegend: false,
    inlineLegend: false,
    size: 'md',
    disabled: false,
  },
  render: (args: CspSegmentedControlProps) => ({
    components: { CspSegmentedControl },
    setup() {
      const model = ref(args.modelValue)
      watch(() => args.modelValue, (value) => {
        model.value = value
      })
      return { args, model }
    },
    template: '<CspSegmentedControl v-bind="args" v-model="model" />',
  }),
}

export default meta
type Story = StoryObj<CspSegmentedControlProps>

export const Default: Story = {}

export const InlineLegend: Story = {
  args: { inlineLegend: true },
}

export const NoLegend: Story = {
  args: { hideLegend: true },
}

export const WithIcons: Story = {
  args: { options: ICON_OPTIONS, modelValue: 'grille', legend: 'Affichage', hideLegend: true },
}

export const Sizes: Story = {
  render: () => ({
    components: { CspSegmentedControl },
    setup() {
      const md = ref('grille')
      const sm = ref('grille')
      return { md, sm, options: ICON_OPTIONS }
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="md" :options="options" legend="Taille md" inline-legend />
        <CspSegmentedControl v-model="sm" :options="options" legend="Taille sm" inline-legend size="sm" />
      </div>
    `,
  }),
}

export const States: Story = {
  render: () => ({
    components: { CspSegmentedControl },
    setup() {
      const partial = ref('option-1')
      const disabled = ref('option-1')
      const options = [...DEFAULT_OPTIONS.slice(0, 2), { value: 'option-3', label: 'Option 3', disabled: true }]
      return { partial, disabled, options, DEFAULT_OPTIONS }
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 1rem; align-items: flex-start;">
        <CspSegmentedControl v-model="partial" :options="options" legend="Une option désactivée" inline-legend />
        <CspSegmentedControl v-model="disabled" :options="DEFAULT_OPTIONS" legend="Groupe désactivé" inline-legend disabled />
      </div>
    `,
  }),
}
