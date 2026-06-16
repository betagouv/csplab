import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'

type CspSelectProps = ComponentPropsAndSlots<typeof CspSelect>

const DEMO_OPTIONS = [
  { value: 'option-1', label: 'Option 1' },
  { value: 'option-2', label: 'Option 2' },
  { value: 'option-3', label: 'Option 3' },
  { value: 'option-4', label: 'Option 4' },
  { value: 'option-5', label: 'Option 5', disabled: true },
]

const meta = {
  title: 'Éléments/Génériques/CspSelect',
  component: CspSelect,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['modelValue', 'options', 'placeholder', 'size', 'disabled', 'error', 'errorMessage', 'label'],
    },
    docs: {
      description: {
        component: 'Sélecteur générique construit sur la primitive `reka-ui` Select. Gère le focus, la navigation clavier et l\'accessibilité. Contrôlé via `v-model`.',
      },
    },
  },
  argTypes: {
    modelValue: {
      control: { type: 'text' },
      description: 'Valeur sélectionnée (v-model).',
      table: {
        type: { summary: 'string' },
      },
    },
    options: {
      control: false,
      description: 'Liste des options. Chaque option a une `value`, un `label` et un `disabled` optionnel.',
      table: {
        type: { summary: 'CspSelectOption[]' },
      },
    },
    placeholder: {
      control: { type: 'text' },
      description: 'Texte affiché quand aucune valeur n\'est sélectionnée.',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'Sélectionner…' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspSelectProps['size']>[],
      description: 'Taille du déclencheur.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive le sélecteur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    error: {
      control: { type: 'boolean' },
      description: 'Affiche l\'état d\'erreur.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    errorMessage: {
      control: { type: 'text' },
      description: 'Message d\'erreur affiché sous le sélecteur si `error` est vrai.',
      table: {
        type: { summary: 'string' },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Libellé visible au-dessus du sélecteur.',
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
    options: DEMO_OPTIONS,
    placeholder: 'Sélectionner…',
    size: 'md',
    disabled: false,
    error: false,
    label: 'Libellé sélecteur',
  },
  render: (args: CspSelectProps) => ({
    components: { CspSelect },
    setup() {
      const value = ref(args.modelValue ?? '')

      watch(
        () => args.modelValue,
        (next) => { value.value = next ?? '' },
      )

      return { args, value }
    },
    template: `
      <div class="max-w-xs">
        <CspSelect v-bind="args" v-model="value" />
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspSelectProps>

const SIZES = ['sm', 'md', 'lg'] as const

export const Default: Story = {
  name: 'Par défaut',
}

export const Sizes: Story = {
  name: 'Tailles',
  render: (args: CspSelectProps) => ({
    components: { CspSelect },
    setup() {
      return { args, sizes: SIZES, options: DEMO_OPTIONS }
    },
    template: `
      <div class="flex flex-col gap-6 max-w-xs">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-xs text-text-mention-grey">{{ s }}</p>
          <CspSelect v-bind="args" :size="s" :options="options" />
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}

export const States: Story = {
  name: 'États',
  render: () => ({
    components: { CspSelect },
    setup() {
      return { options: DEMO_OPTIONS }
    },
    template: `
      <div class="flex flex-col gap-8 max-w-xs">
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Par défaut</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Sélectionner…" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Sélecteur avec valeur sélectionnée</p>
          <CspSelect label="Libellé sélecteur" :options="options" model-value="option-1" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Désactivé</p>
          <CspSelect label="Libellé sélecteur" :options="options" placeholder="Désactivé" :disabled="true" />
        </div>
        <div>
          <p class="text-xs mb-4 text-text-mention-grey">Erreur</p>
          <CspSelect
            label="Libellé sélecteur"
            :options="options"
            :error="true"
            error-message="Ce champ est requis."
            placeholder="Sélectionner…"
          />
        </div>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}
