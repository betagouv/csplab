import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'

type CspTableToolbarProps = ComponentPropsAndSlots<typeof CspTableToolbar>

const meta = {
  title: 'Éléments/Génériques/CspTableToolbar',
  component: CspTableToolbar,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Barre d\'outils à placer immédiatement au-dessus d\'une table : compteur à gauche, recherche et actions à droite. Quand `selectionCount` est renseigné, la barre bascule en mode sélection et affiche le slot `selection-actions` pour les actions en lot.',
      },
    },
  },
  argTypes: {
    count: {
      control: { type: 'text' },
      description: 'Libellé du compteur affiché à gauche (remplaçable par le slot `status`).',
      table: { type: { summary: 'string' } },
    },
    selectionCount: {
      control: { type: 'number' },
      description: 'Nombre d\'éléments sélectionnés ; au-dessus de zéro, la barre passe en mode sélection.',
      table: { type: { summary: 'number' }, defaultValue: { summary: '0' } },
    },
    bordered: {
      control: { type: 'boolean' },
      description: 'Bordure haute de séparation ; à désactiver quand la barre suit immédiatement une autre bordure (p. ex. la barre d\'onglets).',
      table: { type: { summary: 'boolean' }, defaultValue: { summary: 'true' } },
    },
  },
}

export default meta

type Story = StoryObj<CspTableToolbarProps>

export const ParDefaut: Story = {
  args: {
    count: '12 éléments',
  },
  render: args => ({
    components: { CspTableToolbar, CspButton, CspInput },
    setup: () => ({ args }),
    template: `
      <CspTableToolbar v-bind="args">
        <CspInput
          type="search"
          aria-label="Rechercher un élément"
          placeholder="Rechercher un élément"
          style="min-width: 20rem"
        />
        <CspButton label="Ajouter" icon="ri:add-line" is-icon-left />
      </CspTableToolbar>
    `,
  }),
}

export const ModeSelection: Story = {
  args: {
    count: '12 éléments',
    selectionCount: 3,
  },
  render: args => ({
    components: { CspTableToolbar, CspButton },
    setup: () => ({ args }),
    template: `
      <CspTableToolbar v-bind="args">
        <template #selection-actions>
          <CspButton label="Exporter" variant="secondary" />
          <CspButton label="Supprimer" variant="secondary" icon="ri:delete-bin-line" is-icon-left />
        </template>
      </CspTableToolbar>
    `,
  }),
}
