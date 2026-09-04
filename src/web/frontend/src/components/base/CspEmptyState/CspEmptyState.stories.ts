import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'

type CspEmptyStateProps = ComponentPropsAndSlots<typeof CspEmptyState>

const meta = {
  title: 'Éléments/Génériques/CspEmptyState',
  component: CspEmptyState,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['title', 'description', 'icon'],
    },
    docs: {
      description: {
        component: 'État vide partagé : icône, titre, description et action optionnelles. À utiliser partout où une zone n\'a pas encore de contenu.',
      },
    },
  },
}

export default meta
type Story = StoryObj<CspEmptyStateProps>

export const Default: Story = {
  name: 'Par défaut',
  args: {
    title: 'Aucun élément',
    description: 'Les éléments créés apparaîtront ici.',
  },
}

export const AvecAction: Story = {
  name: 'Avec action',
  args: {
    title: 'Aucun résultat',
    icon: 'ri:search-line',
  },
  render: (args: CspEmptyStateProps) => ({
    components: { CspEmptyState, CspButton },
    setup() {
      return { args }
    },
    template: `
      <CspEmptyState v-bind="args">
        <template #action>
          <CspButton label="Réinitialiser les filtres" variant="secondary" />
        </template>
      </CspEmptyState>
    `,
  }),
}
