import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import { ref, watch } from 'vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'

type CspCheckboxGroupProps = ComponentPropsAndSlots<typeof CspCheckboxGroup>

const DEFAULT_OPTIONS = [
  { value: 'design', label: 'Design' },
  { value: 'dev', label: 'Développement' },
  { value: 'product', label: 'Produit' },
  { value: 'data', label: 'Données' },
]

const meta = {
  title: 'Éléments/Génériques/CspCheckboxGroup',
  component: CspCheckboxGroup,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'options', 'label', 'name', 'size', 'disabled', 'error', 'errorMessage'],
    },
    docs: {
      description: {
        component: 'Groupe de cases à cocher pour une sélection multiple. Liez le tableau des valeurs sélectionnées via `v-model`. Si aucun `label` visuel n\'est rendu, fournissez un nom accessible au fieldset via `aria-label`.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'object' },
      description: 'Valeurs actuellement cochées.',
      table: {
        type: { summary: 'string[]' },
        defaultValue: { summary: '[]' },
      },
    },
    options: {
      control: { type: 'object' },
      description: 'Liste des options disponibles.',
      table: {
        type: { summary: '{ value: string; label: string; disabled?: boolean }[]' },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Légende visible pour le groupe (rendue via une balise `<legend>`).',
      table: {
        type: { summary: 'string' },
      },
    },
    name: {
      control: { type: 'text' },
      description: 'Nom HTML partagé par les cases à cocher pour une soumission de formulaire native.',
      table: {
        type: { summary: 'string' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive l\'ensemble du groupe.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'],
      description: 'Taille des cases à cocher.',
      table: {
        type: { summary: '\'sm\' | \'md\' | \'lg\'' },
        defaultValue: { summary: '\'md\'' },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche le groupe en état d\'erreur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    errorMessage: {
      control: { type: 'text' },
      description: 'Message d\'erreur optionnel, affiché lorsque `error` est actif.',
      table: {
        type: { summary: 'string' },
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
    modelValue: ['design'],
    options: DEFAULT_OPTIONS,
    label: 'Domaines',
    name: 'domains',
    disabled: false,
    size: 'md',
    error: false,
  },
  render: (args: CspCheckboxGroupProps) => ({
    components: { CspCheckboxGroup },
    setup() {
      const selected = ref<string[]>(Array.isArray(args.modelValue) ? [...args.modelValue] : [])

      watch(
        () => args.modelValue,
        (value) => {
          if (Array.isArray(value))
            selected.value = [...value]
        },
      )

      return { args, selected }
    },
    template: `
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
      />
    `,
  }),
}

export default meta
type Story = StoryObj<CspCheckboxGroupProps>

export const Default: Story = {}

export const WithDisabledOption: Story = {
  args: {
    options: [
      { value: 'design', label: 'Design' },
      { value: 'dev', label: 'Développement', disabled: true },
      { value: 'product', label: 'Produit' },
    ],
    modelValue: ['design'],
  },
}

export const GroupDisabled: Story = {
  args: {
    disabled: true,
    modelValue: ['design'],
  },
}

export const NoLabel: Story = {
  render: args => ({
    components: { CspCheckboxGroup },
    setup() {
      const selected = ref<string[]>(Array.isArray(args.modelValue) ? [...args.modelValue] : [])

      watch(
        () => args.modelValue,
        (value) => {
          if (Array.isArray(value))
            selected.value = [...value]
        },
      )

      return { args, selected }
    },
    template: `
      <CspCheckboxGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Domaines"
      />
    `,
  }),
}

export const Sizes: Story = {
  render: () => ({
    components: { CspCheckboxGroup },
    template: `
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="sm"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="md"
          />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspCheckboxGroup
            :model-value="['a']"
            :options="[{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }]"
            size="lg"
          />
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const WithError: Story = {
  args: {
    modelValue: [],
    error: true,
    errorMessage: 'Veuillez sélectionner au moins une option.',
  },
}
