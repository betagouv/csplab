import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'

type CspSkeletonProps = ComponentPropsAndSlots<typeof CspSkeleton>

const meta = {
  title: 'Éléments/Génériques/CspSkeleton',
  component: CspSkeleton,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['width', 'height', 'variant'],
    },
    docs: {
      description: {
        component: 'Bloc de chargement neutre qui réserve l\'espace du contenu à venir, pour éviter les décalages de mise en page (layout shift). Dimensionner au plus proche du contenu final. La variante `text` prend la hauteur de ligne de son conteneur et ignore `height`.',
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
    variant: {
      control: { type: 'radio' },
      options: ['block', 'text'] satisfies NonNullable<CspSkeletonProps['variant']>[],
      description: 'Bloc à la hauteur donnée, ou ligne de texte à la hauteur de ligne de son conteneur.',
      table: { defaultValue: { summary: 'block' } },
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

export const Text: Story = {
  name: 'Ligne de texte',
  render: () => ({
    components: { CspSkeleton },
    template: `
      <p style="margin: 0; font-size: 1.125rem;">
        <CspSkeleton width="16rem" variant="text" />
      </p>
    `,
  }),
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
