import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'

type CspAsyncSectionProps = ComponentPropsAndSlots<typeof CspAsyncSection>

const meta = {
  title: 'Compositions/Génériques/CspAsyncSection',
  component: CspAsyncSection,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['pending', 'errorTitle', 'loadingLabel', 'minHeight'],
    },
    docs: {
      description: {
        component: 'Section asynchrone : orchestre le contrat skeleton (pending) → CspErrorState (error) → contenu, avec zone de chargement accessible (role="status") et hauteur réservable.',
      },
    },
  },
}

export default meta
type Story = StoryObj<CspAsyncSectionProps>

function renderSection(args: CspAsyncSectionProps) {
  return {
    components: { CspAsyncSection, CspSkeletonTable },
    setup() {
      return { args }
    },
    template: `
      <CspAsyncSection v-bind="args">
        <template #skeleton>
          <CspSkeletonTable :rows="4" :columns="3" />
        </template>
        <p>Contenu chargé.</p>
      </CspAsyncSection>
    `,
  }
}

export const Chargement: Story = {
  args: {
    pending: true,
    loadingLabel: 'Chargement des données',
  },
  render: renderSection,
}

export const Erreur: Story = {
  args: {
    pending: false,
    error: true,
    errorTitle: 'Une erreur est survenue lors du chargement.',
    minHeight: '16rem',
  },
  render: renderSection,
}

export const Contenu: Story = {
  args: {
    pending: false,
  },
  render: renderSection,
}
