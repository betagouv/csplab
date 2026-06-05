import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import { ref, watch } from 'vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'

type CspSwitchProps = ComponentPropsAndSlots<typeof CspSwitch>

const meta = {
  title: 'Éléments/Génériques/CspSwitch',
  component: CspSwitch,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'label', 'size', 'disabled', 'name', 'id', 'error'],
    },
    docs: {
      description: {
        component: 'Bascule activé/désactivé',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'boolean' },
      description: 'État activé/désactivé (v-model).',
      table: {
        type: { summary: 'boolean' },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Libellé visible associé à la bascule.',
      table: {
        type: { summary: 'string' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive la bascule.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    name: {
      control: { type: 'text' },
      description: 'Attribut `name` pour la soumission de formulaire.',
      table: {
        type: { summary: 'string' },
      },
    },
    id: {
      control: { type: 'text' },
      description: 'Attribut `id` du bouton bascule.',
      table: {
        type: { summary: 'string' },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche la bascule en état d\'erreur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'],
      description: 'Taille de la bascule.',
      table: {
        type: { summary: '\'sm\' | \'md\' | \'lg\'' },
        defaultValue: { summary: '\'md\'' },
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
    modelValue: false,
    label: 'Libellé de la bascule',
    disabled: false,
    name: undefined,
    id: undefined,
    size: 'md',
    error: false,
  },
  render: (args: CspSwitchProps) => ({
    components: { CspSwitch },
    setup() {
      const value = ref(Boolean(args.modelValue))

      watch(
        () => args.modelValue,
        (next) => {
          value.value = Boolean(next)
        },
      )

      return { args, value }
    },
    template: `
      <CspSwitch v-bind="args" v-model="value" />
    `,
  }),
}

export default meta
type Story = StoryObj<CspSwitchProps>

export const Default: Story = {}

export const Disabled: Story = {
  args: {
    disabled: true,
  },
}

export const WithError: Story = {
  args: {
    error: true,
  },
}

export const Sizes: Story = {
  render: () => ({
    components: { CspSwitch },
    setup() {
      const a = ref(true)
      const b = ref(true)
      const c = ref(true)
      return { a, b, c }
    },
    template: `
      <div style="display: flex; gap: 3rem; align-items: flex-start;">
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">sm</span>
          <CspSwitch v-model="a" label="Option" size="sm" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">md</span>
          <CspSwitch v-model="b" label="Option" size="md" />
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          <span style="font-size: 0.75rem; color: var(--text-mention-grey);">lg</span>
          <CspSwitch v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}
