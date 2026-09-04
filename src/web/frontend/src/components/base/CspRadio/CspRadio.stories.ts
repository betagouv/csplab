import type { StoryObj } from '@storybook/vue3-vite'
import { RadioGroupRoot } from 'reka-ui'
import { ref } from 'vue'
import CspRadio from '@/components/base/CspRadio/CspRadio.vue'

const meta = {
  title: 'Éléments/Génériques/CspRadio',
  component: CspRadio,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['value', 'label', 'size', 'disabled', 'error'],
    },
    docs: {
      description: {
        component: 'Bouton radio basé sur reka-ui. Doit être utilisé à l\'intérieur de `CspRadioGroup` (ou d\'un `RadioGroupRoot`). La navigation clavier entre les éléments (flèches) et la gestion du nom de formulaire sont assurées par le groupe parent.',
      },
    },
  },
  argTypes: {
    value: {
      control: { type: 'text' },
      description: 'Valeur de cet élément radio.',
      table: {
        type: { summary: 'string' },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Libellé texte visible associé au bouton radio.',
      table: {
        type: { summary: 'string' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive ce bouton radio.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'],
      description: 'Taille du bouton radio.',
      table: {
        type: { summary: '\'sm\' | \'md\' | \'lg\'' },
        defaultValue: { summary: '\'md\'' },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche le bouton radio en état d\'erreur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
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
    value: 'option-a',
    label: 'Option A',
    disabled: false,
    size: 'md',
    error: false,
  },
  render: (args: Record<string, unknown>) => ({
    components: { CspRadio, RadioGroupRoot },
    setup() {
      const selected = ref('option-a')
      return { args, selected }
    },
    template: `
      <RadioGroupRoot v-model="selected">
        <CspRadio v-bind="args" />
      </RadioGroupRoot>
    `,
  }),
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const Disabled: Story = {
  args: {
    disabled: true,
  },
}

export const Sizes: Story = {
  render: () => ({
    components: { CspRadio, RadioGroupRoot },
    setup() {
      const sizes = ['sm', 'md', 'lg']
      const selected = ref('option-md')
      return { sizes, selected }
    },
    template: `
      <RadioGroupRoot
        v-model="selected"
        class="flex flex-row gap-12"
      >
      <div
        v-for="size in sizes"
        :key="size"
      >
        <div class="h-12 flex items-center">
            <CspRadio
              :value="'option-' + size"
              :label="'Option ' + size.toUpperCase()"
              :size="size"
            />
          </div>
        </div>
      </RadioGroupRoot>
    `,
  }),
}

export const WithError: Story = {
  args: {
    error: true,
  },
}
