import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'

type CspPageHeaderProps = ComponentPropsAndSlots<typeof CspPageHeader>

const meta = {
  title: 'Compositions/Génériques/CspPageHeader',
  component: CspPageHeader,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['title', 'breadcrumb'],
    },
    docs: {
      description: {
        component: 'En-tête de page : fil d’Ariane + titre, avec des slots optionnels `#actions`, `#subtitle` et `#tabs`. Le titre passe par la prop `title` ; le slot `#title` permet un titre enrichi (badge, statut…).',
      },
    },
  },
  argTypes: {
    title: {
      control: { type: 'text' },
      description: 'Titre de la page (rendu dans le `<h1>`). Ignoré si le slot `#title` est fourni.',
      table: { type: { summary: 'string' } },
    },
    breadcrumb: {
      control: { type: 'object' },
      description: 'Maillons du fil d’Ariane, délégués à CspBreadcrumb.',
      table: { type: { summary: '{ label: string; to?: RouteLocationRaw }[]' } },
    },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
  },
  args: {
    title: 'Titre de la page',
    breadcrumb: [
      { label: 'Accueil', to: '/' },
      { label: 'Section' },
      { label: 'Page courante' },
    ],
  },
}

export default meta
type Story = StoryObj<CspPageHeaderProps>

export const Default: Story = {
  name: 'Par défaut',
}

export const WithoutBreadcrumb: Story = {
  name: 'Sans fil d’Ariane',
  args: {
    breadcrumb: [],
  },
}

export const WithActions: Story = {
  name: 'Avec actions',
  render: (args: CspPageHeaderProps) => ({
    components: { CspPageHeader, CspButton },
    setup() {
      return { args }
    },
    template: `
      <CspPageHeader v-bind="args">
        <template #actions>
          <CspButton variant="tertiary" icon="ri:filter-3-line" label="Action secondaire" :is-icon-left="true" />
          <CspButton icon="ri:add-line" label="Action principale" :is-icon-left="true" />
        </template>
      </CspPageHeader>
    `,
  }),
}

export const WithRichTitle: Story = {
  name: 'Titre enrichi',
  render: (args: CspPageHeaderProps) => ({
    components: { CspPageHeader, CspBadge },
    setup() {
      return { args }
    },
    template: `
      <CspPageHeader v-bind="args">
        <template #title>
          Titre de la page
        </template>
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `,
  }),
}
