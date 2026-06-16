import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import { ref, watch } from 'vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'

type CspTabsProps = ComponentPropsAndSlots<typeof CspTabs>

const DEFAULT_TABS = [
  { value: 'tab-1', label: 'Onglet 1' },
  { value: 'tab-2', label: 'Onglet 2' },
  { value: 'tab-3', label: 'Onglet 3' },
]

const meta = {
  title: 'Éléments/Génériques/CspTabs',
  component: CspTabs,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'tabs', 'defaultValue', 'orientation', 'activationMode'],
    },
    docs: {
      description: {
        component: 'Composant d\'onglets accessible basé sur Reka UI. Le contenu de chaque onglet est fourni via des slots nommés correspondant à la valeur de l\'onglet.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Onglet actuellement actif (v-model).',
      table: {
        type: { summary: 'string' },
      },
    },
    tabs: {
      control: { type: 'object' },
      description: 'Liste des onglets disponibles.',
      table: {
        type: { summary: '{ value: string; label: string; disabled?: boolean }[]' },
      },
    },
    defaultValue: {
      control: { type: 'text' },
      description: 'Valeur de l\'onglet actif par défaut (non contrôlé).',
      table: {
        type: { summary: 'string' },
      },
    },
    orientation: {
      control: { type: 'radio' },
      options: ['horizontal', 'vertical'],
      description: 'Orientation des onglets.',
      table: {
        type: { summary: '\'horizontal\' | \'vertical\'' },
        defaultValue: { summary: '\'horizontal\'' },
      },
    },
    activationMode: {
      control: { type: 'radio' },
      options: ['automatic', 'manual'],
      description: 'Mode d\'activation : automatique au focus ou manuel au clic.',
      table: {
        type: { summary: '\'automatic\' | \'manual\'' },
        defaultValue: { summary: '\'automatic\'' },
      },
    },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
    key: { control: false, table: { disable: true } },
    ref: { control: false, table: { disable: true } },
    ref_for: { control: false, table: { disable: true } },
    ref_key: { control: false, table: { disable: true } },
  },
  args: {
    tabs: DEFAULT_TABS,
    defaultValue: 'tab-1',
    orientation: 'horizontal',
    activationMode: 'automatic',
  },
  render: (args: CspTabsProps) => ({
    components: { CspTabs },
    setup() {
      const selected = ref(args.modelValue ?? args.defaultValue ?? '')

      watch(
        () => args.modelValue,
        (value) => {
          if (value !== undefined)
            selected.value = value
        },
      )

      return { args, selected }
    },
    template: `
      <CspTabs
        v-bind="args"
        v-model="selected"
      >
        <template #tab-1>
          <p>Contenu du premier onglet. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </template>
        <template #tab-2>
          <p>Contenu du deuxième onglet. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </template>
        <template #tab-3>
          <p>Contenu du troisième onglet. Ut enim ad minim veniam, quis nostrud exercitation.</p>
        </template>
      </CspTabs>
    `,
  }),
}

export default meta
type Story = StoryObj<CspTabsProps>

export const Default: Story = {}

export const WithDisabledTab: Story = {
  args: {
    tabs: [
      { value: 'tab-1', label: 'Onglet 1' },
      { value: 'tab-2', label: 'Onglet 2', disabled: true },
      { value: 'tab-3', label: 'Onglet 3' },
    ],
    defaultValue: 'tab-1',
  },
}

export const Vertical: Story = {
  args: {
    orientation: 'vertical',
  },
}

export const ManualActivation: Story = {
  args: {
    activationMode: 'manual',
  },
  parameters: {
    docs: {
      description: {
        story: 'En mode manuel, les onglets ne s\'activent qu\'au clic et non au focus clavier.',
      },
    },
  },
}
