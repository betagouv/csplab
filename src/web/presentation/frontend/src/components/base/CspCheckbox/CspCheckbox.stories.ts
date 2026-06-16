import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'

type CspCheckboxProps = ComponentPropsAndSlots<typeof CspCheckbox>

const meta = {
  title: 'Éléments/Génériques/CspCheckbox',
  component: CspCheckbox,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'label', 'size', 'disabled', 'indeterminate', 'error'],
    },
    docs: {
      description: {
        component: 'Primitive de case à cocher générique. Contrôlée via `modelValue` (v-model). L\'état optionnel `indeterminate` est uniquement visuel et doit être contrôlé par le parent.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'boolean' },
      description: 'État coché (v-model).',
      table: {
        type: {
          summary: 'boolean',
        },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Libellé visible.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive la case à cocher.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    indeterminate: {
      control: { type: 'boolean' },
      description: 'Visuel à trois états : affiche un état indéterminé. Le parent doit le réinitialiser lors d\'une interaction utilisateur.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspCheckboxProps['size']>[],
      description: 'Taille de la case à cocher.',
      table: {
        type: { summary: '\'sm\' | \'md\' | \'lg\'' },
        defaultValue: { summary: '\'md\'' },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche la case à cocher en état d\'erreur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    default: {
      control: false,
      table: {
        disable: true,
      },
    },
    class: {
      control: false,
      table: {
        disable: true,
      },
    },
    style: {
      control: false,
      table: {
        disable: true,
      },
    },
    key: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref_for: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref_key: {
      control: false,
      table: {
        disable: true,
      },
    },
  },
  args: {
    modelValue: false,
    label: 'Accepter les conditions',
    disabled: false,
    indeterminate: false,
    size: 'md',
    error: false,
  },
  render: (args: CspCheckboxProps) => ({
    components: { CspCheckbox },
    setup() {
      const value = ref(Boolean(args.modelValue))
      const isIndeterminate = ref(Boolean(args.indeterminate))

      watch(
        () => args.modelValue,
        (next) => {
          value.value = Boolean(next)
        },
      )

      watch(
        () => args.indeterminate,
        (next) => {
          isIndeterminate.value = Boolean(next)
        },
      )

      function handleUpdate(nextValue: boolean) {
        value.value = nextValue

        // Indeterminate is display-only: the parent should clear it after interaction.
        if (isIndeterminate.value) {
          isIndeterminate.value = false
        }
      }

      return {
        args,
        value,
        isIndeterminate,
        handleUpdate,
      }
    },
    template: `
      <div class="h-12 flex items-center">
        <CspCheckbox
          :label="args.label"
          :disabled="args.disabled"
          :indeterminate="isIndeterminate"
          :size="args.size"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspCheckboxProps>

export const Default: Story = {}

export const Disabled: Story = {
  args: {
    disabled: true,
  },
}

export const Indeterminate: Story = {
  args: {
    indeterminate: true,
    modelValue: false,
  },
}

export const States: Story = {
  render: () => ({
    components: { CspCheckbox },
    setup() {
      const checked = ref(true)
      const unchecked = ref(false)
      return { checked, unchecked }
    },
    template: `
      <div class="flex flex-col gap-4">
        <CspCheckbox v-model="unchecked" label="Non coché" />
        <CspCheckbox v-model="checked" label="Coché" />
        <CspCheckbox :model-value="false" :indeterminate="true" label="Indéterminé" />
        <CspCheckbox :model-value="false" :disabled="true" label="Désactivé" />
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const Sizes: Story = {
  render: () => ({
    components: { CspCheckbox },
    setup() {
      const a = ref(true)
      const b = ref(true)
      const c = ref(true)
      return { a, b, c }
    },
    template: `
      <div class="flex flex-row gap-12">
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">sm</span>
          <CspCheckbox v-model="a" label="Option" size="sm" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">md</span>
          <CspCheckbox v-model="b" label="Option" size="md" />
        </div>
        <div class="flex flex-col gap-2">
          <span class="text-xs text-text-mention-grey">lg</span>
          <CspCheckbox v-model="c" label="Option" size="lg" />
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}
