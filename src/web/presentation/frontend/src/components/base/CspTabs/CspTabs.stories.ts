import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTabsList from '@/components/base/CspTabs/CspTabsList.vue'
import CspTabsPanels from '@/components/base/CspTabs/CspTabsPanels.vue'

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
        component: 'Composant d\'onglets accessible basé sur Reka UI. Usage monolithique : passez `tabs` et fournissez un slot nommé par valeur d\'onglet. Usage composé : placez `CspTabsList` et `CspTabsPanels` dans le slot par défaut pour répartir la barre et les panneaux dans des régions de layout différentes (p. ex. la barre dans un en-tête de page).',
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
        type: { summary: '{ value: string; label: string; icon?: string; disabled?: boolean }[]' },
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
          <p>Contenu du premier onglet.</p>
        </template>
        <template #tab-2>
          <p>Contenu du deuxième onglet.</p>
        </template>
        <template #tab-3>
          <p>Contenu du troisième onglet.</p>
        </template>
      </CspTabs>
    `,
  }),
}

export default meta
type Story = StoryObj<CspTabsProps>

export const Default: Story = {
  name: 'Usage monolithique',
}

export const Composed: Story = {
  name: 'Usage composé',
  parameters: {
    docs: {
      description: {
        story: 'Usage composé : la barre (CspTabsList) et les panneaux (CspTabsPanels) sont rendus séparément tout en partageant l’état, ici la barre dans un en-tête simulé et les panneaux en dessous.',
      },
    },
  },
  render: (args: CspTabsProps) => ({
    components: { CspTabs, CspTabsList, CspTabsPanels },
    setup() {
      const selected = ref(args.defaultValue ?? 'tab-1')
      return { args, selected }
    },
    template: `
      <CspTabs v-model="selected" :default-value="args.defaultValue">
        <div style="border:1px solid var(--border-default-grey);padding:1rem;margin-bottom:1rem">
          <strong>En-tête de page</strong>
          <CspTabsList :tabs="args.tabs" />
        </div>
        <CspTabsPanels :tabs="args.tabs">
          <template #tab-1><p>Contenu du premier onglet.</p></template>
          <template #tab-2><p>Contenu du deuxième onglet.</p></template>
          <template #tab-3><p>Contenu du troisième onglet.</p></template>
        </CspTabsPanels>
      </CspTabs>
    `,
  }),
}

export const WithDisabledTab: Story = {
  name: 'Avec onglet désactivé',
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
  name: 'Orientation verticale',
  args: {
    orientation: 'vertical',
  },
}

export const ManualActivation: Story = {
  name: 'Activation manuelle',
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

export const WithIcons: Story = {
  name: 'Avec icônes',
  args: {
    tabs: [
      { value: 'tab-1', label: 'Accueil', icon: 'ri:home-line' },
      { value: 'tab-2', label: 'Paramètres', icon: 'ri:settings-3-line' },
      { value: 'tab-3', label: 'Utilisateurs', icon: 'ri:user-line' },
    ],
    defaultValue: 'tab-1',
  },
}
