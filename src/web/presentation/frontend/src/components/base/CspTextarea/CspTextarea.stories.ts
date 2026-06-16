import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'

type CspTextareaProps = ComponentPropsAndSlots<typeof CspTextarea>

const TEXTAREA_ID = 'base-textarea-story'

const meta = {
  title: 'Éléments/Génériques/CspTextarea',
  component: CspTextarea,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'placeholder', 'rows', 'disabled', 'error', 'errorMessage', 'resize', 'label'],
    },
    docs: {
      description: {
        component: 'Primitive de zone de texte générique, contrôlée via `v-model` (`modelValue` / `update:modelValue`).',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Valeur actuelle de la zone de texte (v-model).',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    placeholder: {
      control: { type: 'text' },
      description: 'Espace réservé natif affiché lorsque le champ est vide.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    rows: {
      control: { type: 'number', min: 1, max: 20 },
      description: 'Nombre de lignes visibles.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '4',
        },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive la saisie de l\'utilisateur.',
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
    resize: {
      control: { type: 'radio' },
      options: ['none', 'vertical', 'horizontal', 'both'] satisfies NonNullable<CspTextareaProps['resize']>[],
      description: 'Comportement de redimensionnement natif.',
      table: {
        type: {
          summary: 'none | vertical | horizontal | both',
        },
        defaultValue: {
          summary: 'vertical',
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
    placeholder: 'Tapez votre message…',
    rows: 4,
    disabled: false,
    resize: 'vertical',
  },
  render: (args: CspTextareaProps) => ({
    components: { CspTextarea },
    setup() {
      const value = ref(args.modelValue ?? '')

      watch(
        () => args.modelValue,
        (nextValue) => {
          value.value = nextValue ?? ''
        },
      )

      function onUpdate(nextValue: string) {
        value.value = nextValue
      }

      return { args, value, onUpdate, textareaId: TEXTAREA_ID }
    },
    template: `
      <div class="w-96">
        <label
          :for="textareaId"
          class="block mb-2 text-sm font-medium"
        >
          Message
        </label>
        <CspTextarea
          v-bind="args"
          :id="textareaId"
          :model-value="value"
          @update:model-value="onUpdate"
        />
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspTextareaProps>

const RESIZES = ['none', 'vertical', 'horizontal', 'both'] as const

export const Default: Story = {}

export const States: Story = {
  render: args => ({
    components: { CspTextarea },
    setup() {
      return { args }
    },
    template: `
      <div class="flex flex-col gap-8 max-w-xl">
        <div>
          <p class="mb-2">Par défaut</p>
          <CspTextarea v-bind="args" placeholder="Tapez votre message…" />
        </div>
        <div>
          <p class="mb-2">Désactivé</p>
          <CspTextarea v-bind="args" :disabled="true" placeholder="Désactivé" />
        </div>
      </div>
    `,
  }),
}

export const Resizes: Story = {
  render: args => ({
    components: { CspTextarea },
    setup() {
      return { args, resizes: RESIZES }
    },
    template: `
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in resizes"
          :key="r"
        >
          <p class="mb-2">Redimensionnement : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :resize="r"
            :rows="3"
            :modelValue="'Un texte sur\\nplusieurs lignes.'"
          />
        </div>
      </div>
    `,
  }),
}

export const Rows: Story = {
  render: args => ({
    components: { CspTextarea },
    setup() {
      const rowsVariants = [2, 4, 8] as const
      return { args, rowsVariants }
    },
    template: `
      <div class="flex flex-col gap-8 max-w-xl">
        <div
          v-for="r in rowsVariants"
          :key="r"
        >
          <p class="mb-2">Lignes (rows) : {{ r }}</p>
          <CspTextarea
            v-bind="args"
            :rows="r"
            :modelValue="'Contenu de démonstration'"
          />
        </div>
      </div>
    `,
  }),
}

export const WithError: Story = {
  args: {
    label: 'Message',
    error: true,
    errorMessage: 'Ce champ est obligatoire.',
    placeholder: 'Tapez votre message…',
    modelValue: '',
  },
  render: (args: CspTextareaProps) => ({
    components: { CspTextarea },
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
      <div class="max-w-xl">
        <CspTextarea
          v-bind="args"
          :model-value="value"
          @update:model-value="value = $event"
        />
      </div>
    `,
  }),
}
