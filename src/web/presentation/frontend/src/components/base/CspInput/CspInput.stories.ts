import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'

type CspInputProps = ComponentPropsAndSlots<typeof CspInput>

const meta = {
  title: 'Éléments/Génériques/CspInput',
  component: CspInput,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'type', 'placeholder', 'size', 'disabled', 'error', 'errorMessage', 'id', 'name', 'label'],
    },
    docs: {
      description: {
        component: 'Champ de saisie de texte.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Valeur actuelle (v-model).',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    type: {
      control: { type: 'radio' },
      options: ['text', 'email', 'password', 'search', 'tel', 'url', 'number'] satisfies NonNullable<CspInputProps['type']>[],
      description: 'Type d\'entrée natif.',
      table: {
        type: {
          summary: 'text | email | password | search | tel | url | number',
        },
        defaultValue: {
          summary: 'text',
        },
      },
    },
    placeholder: {
      control: { type: 'text' },
      description: 'Texte d\'espace réservé (placeholder).',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspInputProps['size']>[],
      description: 'Taille de l\'entrée.',
      table: {
        type: {
          summary: 'sm | md | lg',
        },
        defaultValue: {
          summary: 'md',
        },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive l\'entrée.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche le champ en état d\'erreur.',
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
    id: {
      control: { type: 'text' },
      description: 'ID optionnel pour l\'association du label.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    name: {
      control: { type: 'text' },
      description: 'Nom optionnel pour la soumission du formulaire.',
      table: {
        type: {
          summary: 'string',
        },
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
    modelValue: '',
    type: 'text',
    placeholder: 'Saisir un texte',
    size: 'md',
    disabled: false,
    id: 'base-input-story',
    name: 'base-input',
  },
  render: (args: CspInputProps) => ({
    components: { CspInput },
    setup() {
      const value = ref(args.modelValue ?? '')

      watch(
        () => args.modelValue,
        (nextValue) => {
          value.value = nextValue ?? ''
        },
      )

      function handleUpdate(nextValue: string) {
        value.value = nextValue
      }

      return { args, value, handleUpdate }
    },
    template: `
      <div class="w-96">
        <label
          class="block mb-2 text-sm font-medium"
          :for="args.id"
        >
          Libellé
        </label>
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="handleUpdate"
        />
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspInputProps>

const SIZES = ['sm', 'md', 'lg'] as const
const TYPES = ['text', 'email', 'password', 'search', 'tel', 'url', 'number'] as const

export const Default: Story = {}

export const Disabled: Story = {
  args: {
    disabled: true,
    modelValue: 'Valeur non modifiable',
  },
}

export const Sizes: Story = {
  render: args => ({
    components: { CspInput },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex flex-col gap-6">
        <div
          v-for="s in sizes"
          :key="s"
          class="w-96"
        >
          <p class="mb-2">{{ s }}</p>
          <CspInput
            v-bind="args"
            :size="s"
            :model-value="'Texte'"
          />
        </div>
      </div>
    `,
  }),
}

export const Types: Story = {
  render: args => ({
    components: { CspInput },
    setup() {
      return { types: TYPES, args }
    },
    template: `
      <div class="flex flex-col gap-6">
        <div
          v-for="t in types"
          :key="t"
          class="w-96"
        >
          <p class="mb-2">{{ t }}</p>
          <CspInput
            v-bind="args"
            :type="t"
            :model-value="t === 'password' ? 'secret' : 'Texte'"
          />
        </div>
      </div>
    `,
  }),
}

export const WithError: Story = {
  args: {
    label: 'Libellé input',
    error: true,
    errorMessage: 'Ce champ est obligatoire.',
    modelValue: '',
  },
  render: (args: CspInputProps) => ({
    components: { CspInput },
    setup() {
      const value = ref(args.modelValue ?? '')

      watch(
        () => args.modelValue,
        (nextValue) => {
          value.value = nextValue ?? ''
        },
      )

      return { args, value }
    },
    template: `
      <div class="w-96">
        <CspInput
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `,
  }),
}
