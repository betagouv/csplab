import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'

type CspErrorStateProps = ComponentPropsAndSlots<typeof CspErrorState>

const meta = {
  title: 'Éléments/Génériques/CspErrorState',
  component: CspErrorState,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['title', 'description', 'icon'],
    },
    docs: {
      description: {
        component: 'État d\'erreur partagé (role="alert") : icône, titre, description et action optionnelles. Remplace les messages d\'erreur textuels ad hoc.',
      },
    },
  },
}

export default meta
type Story = StoryObj<CspErrorStateProps>

export const Default: Story = {
  name: 'Par défaut',
  args: {},
}

export const AvecRetry: Story = {
  name: 'Avec action de relance',
  args: {
    title: 'Une erreur est survenue lors du chargement des données.',
  },
  render: (args: CspErrorStateProps) => ({
    components: { CspErrorState, CspButton },
    setup() {
      return { args }
    },
    template: `
      <CspErrorState v-bind="args">
        <template #action>
          <CspButton label="Réessayer" variant="secondary" />
        </template>
      </CspErrorState>
    `,
  }),
}
