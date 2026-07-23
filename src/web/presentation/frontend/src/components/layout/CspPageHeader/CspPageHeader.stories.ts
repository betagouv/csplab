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
        component: 'En-tête de page : fil d’Ariane + titre (prop `title`), avec un lien de retour optionnel (`backLink`), les slots `#actions` et `#subtitle`, et des skeletons de chargement (`showTitleSkeleton`, `showSubtitleSkeleton`).',
      },
    },
  },
  argTypes: {
    title: {
      control: { type: 'text' },
      description: 'Titre de la page (rendu dans le `<h1>`).',
      table: { type: { summary: 'string' } },
    },
    breadcrumb: {
      control: { type: 'object' },
      description: 'Maillons du fil d’Ariane, délégués à CspBreadcrumb.',
      table: { type: { summary: '{ label: string; to?: RouteLocationRaw }[]' } },
    },
    backLink: {
      control: { type: 'object' },
      description: 'Lien de retour optionnel affiché avant le titre.',
      table: { type: { summary: '{ to: RouteLocationRaw; label: string }' } },
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

export const WithSubtitle: Story = {
  name: 'Avec sous-titre',
  render: (args: CspPageHeaderProps) => ({
    components: { CspPageHeader, CspBadge },
    setup() {
      return { args }
    },
    template: `
      <CspPageHeader v-bind="args">
        <template #subtitle>
          <span>Métadonnée</span>
          <CspBadge type="success" label="Statut" />
        </template>
      </CspPageHeader>
    `,
  }),
}

export const WithBackLink: Story = {
  name: 'Avec lien de retour',
  args: {
    backLink: { to: '/', label: 'Retour' },
  },
}

export const Loading: Story = {
  name: 'Chargement',
  args: {
    showTitleSkeleton: true,
    showSubtitleSkeleton: true,
  },
}
