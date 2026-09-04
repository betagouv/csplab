import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

type CspRadioGroupProps = ComponentPropsAndSlots<typeof CspRadioGroup>

const DEFAULT_OPTIONS = [
  { value: 'option-1', label: 'Option 1' },
  { value: 'option-2', label: 'Option 2' },
  { value: 'option-3', label: 'Option 3' },
]

const meta = {
  title: 'Éléments/Génériques/CspRadioGroup',
  component: CspRadioGroup,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'options', 'label', 'name', 'size', 'disabled', 'error', 'errorMessage'],
    },
    docs: {
      description: {
        component: 'Groupe de boutons csp-radio pour une sélection unique exclusive. Liez la valeur sélectionnée via `v-model`. Si aucun `label` visuel n\'est rendu, fournissez un nom accessible au fieldset via `aria-label`.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Valeur actuellement sélectionnée.',
      table: {
        type: { summary: 'string' },
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
      description: 'Attribut `name` partagé pour tous les boutons csp-radio du groupe.',
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
      description: 'Libellé du groupe des boutons radio.',
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
    modelValue: 'option-2',
    options: DEFAULT_OPTIONS,
    label: 'Libellé du groupe',
    name: 'size',
    disabled: false,
    size: 'md',
    error: false,
  },
  render: (args: CspRadioGroupProps) => ({
    components: { CspRadioGroup },
    setup() {
      const selected = ref(args.modelValue ?? '')

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
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
      />
    `,
  }),
}

export default meta
type Story = StoryObj<CspRadioGroupProps>

export const Default: Story = {}

export const WithDisabledOption: Story = {
  args: {
    options: [
      { value: 'option-1', label: 'Option 1' },
      { value: 'option-2', label: 'Option 2', disabled: true },
      { value: 'option-3', label: 'Option 3' },
    ],
    modelValue: 'option-1',
  },
}

export const GroupDisabled: Story = {
  args: {
    disabled: true,
    modelValue: 'option-2',
  },
}

export const NoLabel: Story = {
  render: args => ({
    components: { CspRadioGroup },
    setup() {
      const selected = ref(args.modelValue ?? '')

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
      <CspRadioGroup
        v-bind="args"
        v-model="selected"
        :label="undefined"
        aria-label="Libellé du groupe"
      />
    `,
  }),
}

export const Sizes: Story = {
  render: () => ({
    components: { CspRadioGroup },
    setup() {
      const sizes = ['sm', 'md', 'lg']
      const selected = ref('option-1')
      return { sizes, selected }
    },
    template: `
      <div class="flex flex-row gap-12">
        <CspRadioGroup
          v-for="size in sizes"
          :key="size"
          v-model="selected"
          :options="[
            { value: 'option-1', label: 'Option 1' },
            { value: 'option-2', label: 'Option 2' },
            { value: 'option-3', label: 'Option 3' },
          ]"
          :size="size"
        />
      </div>
    `,
  }),
}

export const WithError: Story = {
  args: {
    modelValue: '',
    error: true,
    errorMessage: 'Veuillez sélectionner une option.',
  },
}
