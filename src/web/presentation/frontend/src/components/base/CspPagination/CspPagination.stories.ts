import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { reactive, ref, watch } from 'vue'
import CspPagination from './CspPagination.vue'

type CspPaginationProps = ComponentPropsAndSlots<typeof CspPagination>

interface PaginationDemo {
  name: string
  page: number
  pageCount: number
  siblingCount: number
  showFirstLast: boolean
  showDirectionLabels: boolean
  disabled: boolean
}

function createGalleryRender(demos: PaginationDemo[]) {
  return () => ({
    components: { CspPagination },
    setup() {
      return {
        demos: reactive(demos.map(demo => ({ ...demo }))),
      }
    },
    template: `
      <div class="flex flex-col gap-12 py-4">
        <section
          v-for="demo in demos"
          :key="demo.name"
          class="flex flex-col gap-2"
        >
          <p class="text-sm text-[var(--text-mention-grey)]">{{ demo.name }}</p>
          <CspPagination
            v-model:page="demo.page"
            :page-count="demo.pageCount"
            :sibling-count="demo.siblingCount"
            :show-first-last="demo.showFirstLast"
            :show-direction-labels="demo.showDirectionLabels"
            :disabled="demo.disabled"
          />
        </section>
      </div>
    `,
  })
}

const meta = {
  title: 'Éléments/Génériques/CspPagination',
  component: CspPagination,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['page', 'pageCount', 'siblingCount', 'showFirstLast', 'showDirectionLabels', 'disabled'],
    },
    docs: {
      description: {
        component: 'Pagination basée sur Reka UI et alignée sur les principes DSFR. Le composant expose une API contrôlée via `v-model:page` et gère la navigation clavier, les états désactivés et les attributs ARIA pour l’accessibilité.',
      },
    },
  },
  argTypes: {
    page: {
      control: { type: 'number', min: 1, step: 1 },
      description: 'Page actuellement active.',
      table: {
        type: { summary: 'number' },
      },
    },
    pageCount: {
      control: { type: 'number', min: 1, step: 1 },
      description: 'Nombre total de pages disponibles.',
      table: {
        type: { summary: 'number' },
      },
    },
    siblingCount: {
      control: { type: 'number', min: 0, step: 1 },
      description: 'Nombre de pages voisines affichées autour de la page active.',
      table: {
        type: { summary: 'number' },
        defaultValue: { summary: '1' },
      },
    },
    showFirstLast: {
      control: { type: 'boolean' },
      description: 'Affiche les boutons de première et dernière page.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    showDirectionLabels: {
      control: { type: 'boolean' },
      description: 'Affiche les libellés de navigation « Précédente » et « Suivante » à partir du breakpoint large.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive l’ensemble de la pagination.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
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
    page: 5,
    pageCount: 12,
    siblingCount: 1,
    showFirstLast: true,
    showDirectionLabels: true,
    disabled: false,
  },
  render: (args: CspPaginationProps) => ({
    components: { CspPagination },
    setup() {
      const page = ref(args.page ?? 1)

      watch(
        () => args.page,
        (value) => {
          if (value !== undefined)
            page.value = value
        },
      )

      return { args, page }
    },
    template: `
      <CspPagination
        v-bind="args"
        v-model:page="page"
      />
    `,
  }),
}

export default meta
type Story = StoryObj<CspPaginationProps>

export const Playground: Story = {
  name: 'Par défaut',
}

export const UsagePatterns: Story = {
  name: 'Cas courants',
  render: createGalleryRender([
    {
      name: 'Pagination standard',
      page: 5,
      pageCount: 12,
      siblingCount: 1,
      showFirstLast: true,
      showDirectionLabels: true,
      disabled: false,
    },
    {
      name: 'Peu de pages',
      page: 1,
      pageCount: 2,
      siblingCount: 1,
      showFirstLast: true,
      showDirectionLabels: true,
      disabled: false,
    },
    {
      name: 'Liste longue',
      page: 24,
      pageCount: 48,
      siblingCount: 2,
      showFirstLast: true,
      showDirectionLabels: true,
      disabled: false,
    },
  ]),
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        story: 'Regroupe les formes les plus fréquentes de pagination pour revue rapide du comportement et du rendu.',
      },
    },
  },
}

export const States: Story = {
  name: 'États et options',
  render: createGalleryRender([
    {
      name: 'Sans première et dernière page',
      page: 3,
      pageCount: 8,
      siblingCount: 1,
      showFirstLast: false,
      showDirectionLabels: true,
      disabled: false,
    },
    {
      name: 'État désactivé',
      page: 5,
      pageCount: 12,
      siblingCount: 1,
      showFirstLast: true,
      showDirectionLabels: true,
      disabled: true,
    },
  ]),
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        story: 'Regroupe les variantes d’état et les options d’affichage qui modifient la structure de navigation.',
      },
    },
  },
}

export const DirectionLabels: Story = {
  name: 'Libellés de navigation',
  render: createGalleryRender([
    {
      name: 'Avec libellés',
      page: 5,
      pageCount: 12,
      siblingCount: 1,
      showFirstLast: true,
      showDirectionLabels: true,
      disabled: false,
    },
    {
      name: 'Sans libellés',
      page: 5,
      pageCount: 12,
      siblingCount: 1,
      showFirstLast: true,
      showDirectionLabels: false,
      disabled: false,
    },
  ]),
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        story: 'Compare la présence ou l’absence des libellés directionnels sur les boutons précédent et suivant.',
      },
    },
  },
}
