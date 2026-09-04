import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { computed, ref } from 'vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'

type CspComboboxProps = ComponentPropsAndSlots<typeof CspCombobox>

const DEMO_OPTIONS = [
  { value: 'option-1', label: 'Option 1', description: 'Description de l\'option 1' },
  { value: 'option-2', label: 'Option 2', description: 'Description de l\'option 2' },
  { value: 'option-3', label: 'Option 3', description: 'Description de l\'option 3' },
  { value: 'option-4', label: 'Option 4' },
]

const meta = {
  title: 'Éléments/Génériques/CspCombobox',
  component: CspCombobox,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'hint', 'placeholder', 'emptyLabel', 'actionLabel', 'pending'],
    },
    docs: {
      description: {
        component: 'Champ de recherche avec autocomplétion, construit sur la primitive `reka-ui` Combobox (pattern ARIA combobox : focus conservé dans le champ, navigation par `aria-activedescendant`, annonce du nombre de résultats via une région de statut). Le filtrage est à la charge de l\'appelant (`searchTerm` en v-model). Une option d\'action facultative (`actionLabel`) s\'affiche en fin de liste et émet `action` sans sélectionner de valeur.',
      },
    },
  },
  argTypes: {
    options: {
      control: false,
      description: 'Options affichées. Chaque option a une `value`, un `label` et une `description` optionnelle.',
      table: { type: { summary: 'CspComboboxOption[]' } },
    },
    label: {
      control: { type: 'text' },
      description: 'Libellé du champ.',
      table: { type: { summary: 'string' } },
    },
    hint: {
      control: { type: 'text' },
      description: 'Texte d\'aide sous le libellé, relié au champ par `aria-describedby`.',
      table: { type: { summary: 'string' } },
    },
    actionLabel: {
      control: { type: 'text' },
      description: 'Libellé de l\'option d\'action en fin de liste. `null` pour la masquer.',
      table: { type: { summary: 'string | null' } },
    },
  },
  args: {
    options: DEMO_OPTIONS,
    label: 'Rechercher un élément',
    placeholder: 'Rechercher…',
  },
} satisfies { args: Partial<CspComboboxProps> } & Record<string, unknown>

export default meta

type Story = StoryObj<typeof meta>

function renderCombobox(args: Partial<CspComboboxProps>) {
  return {
    components: { CspCombobox },
    setup() {
      const model = ref<string | null>(null)
      const searchTerm = ref('')
      const filtered = computed(() => {
        const term = searchTerm.value.trim().toLowerCase()
        if (!term)
          return DEMO_OPTIONS
        return DEMO_OPTIONS.filter(o => o.label.toLowerCase().includes(term))
      })
      return { args, model, searchTerm, filtered }
    },
    template: `
      <div style="max-width: 24rem; min-height: 18rem;">
        <CspCombobox
          v-bind="args"
          v-model="model"
          v-model:search-term="searchTerm"
          :options="filtered"
        />
        <p style="margin-top: 1rem; font-size: 0.8125rem; color: var(--text-mention-grey);">
          Sélection : {{ model ?? 'aucune' }}
        </p>
      </div>
    `,
  }
}

export const Default: Story = {
  render: args => renderCombobox(args),
}

export const AvecAction: Story = {
  name: 'Avec option d\'action',
  render: args => renderCombobox({
    ...args,
    actionLabel: 'Créer un nouvel élément',
  }),
  parameters: {
    docs: {
      description: {
        story: 'L\'option d\'action apparaît en fin de liste, séparée des résultats. Elle émet `action` au lieu de sélectionner une valeur.',
      },
    },
  },
}
