import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'

type CspBreadcrumbProps = ComponentPropsAndSlots<typeof CspBreadcrumb>

const meta = {
  title: 'Éléments/Génériques/CspBreadcrumb',
  component: CspBreadcrumb,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['items', 'ariaLabel'],
    },
    docs: {
      description: {
        component: 'Fil d’Ariane. Entièrement piloté par la prop `items` : le dernier maillon sans `to` est marqué comme page courante.',
      },
    },
  },
  argTypes: {
    items: {
      control: { type: 'object' },
      description: 'Maillons du fil d’Ariane. Un maillon sans `to` est rendu en texte (page courante).',
      table: {
        type: { summary: '{ label: string; to?: RouteLocationRaw }[]' },
      },
    },
    ariaLabel: {
      control: { type: 'text' },
      description: 'Libellé accessible de la navigation.',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: '\'Fil d’Ariane\'' },
      },
    },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
  },
  args: {
    items: [
      { label: 'Accueil', to: '/' },
      { label: 'Page courante' },
    ],
  },
}

export default meta
type Story = StoryObj<CspBreadcrumbProps>

export const Default: Story = {
  name: 'Par défaut',
}

export const SingleLevel: Story = {
  name: '1 niveau',
  args: {
    items: [
      { label: 'Page courante' },
    ],
  },
}

export const DeepNesting: Story = {
  name: '4 niveaux',
  args: {
    items: [
      { label: 'Accueil', to: '/' },
      { label: 'Niveau 1', to: '/niveau-1' },
      { label: 'Niveau 2', to: '/niveau-1/niveau-2' },
      { label: 'Page courante' },
    ],
  },
}
