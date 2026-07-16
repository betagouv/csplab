import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'

type CspSkeletonProps = ComponentPropsAndSlots<typeof CspSkeleton>

const meta = {
  title: 'Éléments/Génériques/CspSkeleton',
  component: CspSkeleton,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['width', 'height'],
    },
    docs: {
      description: {
        component: 'Bloc de chargement neutre qui réserve l\'espace du contenu à venir, pour éviter les décalages de mise en page (layout shift). Dimensionner au plus proche du contenu final.',
      },
    },
  },
  argTypes: {
    width: {
      control: { type: 'text' },
      description: 'Largeur CSS du bloc.',
      table: {
        type: {
          summary: 'string',
        },
        defaultValue: {
          summary: '100%',
        },
      },
    },
    height: {
      control: { type: 'text' },
      description: 'Hauteur CSS du bloc.',
      table: {
        type: {
          summary: 'string',
        },
        defaultValue: {
          summary: '1rem',
        },
      },
    },
  },
}

export default meta
type Story = StoryObj<CspSkeletonProps>

export const Default: Story = {
  name: 'Par défaut',
  args: {
    width: '16rem',
    height: '1rem',
  },
}

export const TitleAndMeta: Story = {
  name: 'Titre et métadonnées',
  render: () => ({
    components: { CspSkeleton },
    template: `
      <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <CspSkeleton width="20rem" height="2rem" />
        <CspSkeleton width="28rem" height="1.375rem" />
      </div>
    `,
  }),
}
