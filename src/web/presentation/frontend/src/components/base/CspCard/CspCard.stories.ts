import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'

type CspCardProps = ComponentPropsAndSlots<typeof CspCard>

const meta = {
  title: 'Éléments/Génériques/CspCard',
  component: CspCard,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['variant', 'size', 'as', 'title', 'titleAs', 'description', 'href'],
    },
    docs: {
      description: {
        component: 'Carte générique pour présenter du contenu avec un titre, une description et des actions associées.',
      },
    },
  },
  argTypes: {
    variant: {
      control: { type: 'radio' },
      options: ['default', 'alt'] satisfies NonNullable<CspCardProps['variant']>[],
      description: 'Style visuel.',
      table: {
        type: { summary: 'default | alt' },
        defaultValue: { summary: 'default' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspCardProps['size']>[],
      description: 'Taille de la carte : ajuste padding, interlignes et typographie.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
      },
    },
    as: {
      control: { type: 'radio' },
      options: ['article', 'section', 'div'] satisfies NonNullable<CspCardProps['as']>[],
      description: 'Élément racine rendu.',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'article' },
      },
    },
    title: {
      control: { type: 'text' },
      description: 'Titre de la carte. Surclassé par le slot `title`.',
      table: {
        type: { summary: 'string | null' },
        defaultValue: { summary: 'null' },
      },
    },
    titleAs: {
      control: { type: 'radio' },
      options: ['h2', 'h3', 'h4', 'h5', 'h6'] satisfies NonNullable<CspCardProps['titleAs']>[],
      description: 'Niveau de titre rendu (accessibilité).',
      table: {
        type: { summary: 'h2 | h3 | h4 | h5 | h6' },
        defaultValue: { summary: 'h3' },
      },
    },
    description: {
      control: { type: 'text' },
      description: 'Description de la carte. Surclassée par le slot `description`.',
      table: {
        type: { summary: 'string | null' },
        defaultValue: { summary: 'null' },
      },
    },
    href: {
      control: { type: 'text' },
      description: 'Active le motif « carte cliquable » : le titre devient un lien couvrant toute la carte.',
      table: {
        type: { summary: 'string' },
      },
    },
    default: { control: false, table: { disable: true } },
    start: { control: false, table: { disable: true } },
    end: { control: false, table: { disable: true } },
    footer: { control: false, table: { disable: true } },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
    key: { control: false, table: { disable: true } },
    ref: { control: false, table: { disable: true } },
    ref_for: { control: false, table: { disable: true } },
    ref_key: { control: false, table: { disable: true } },
  },
  args: {
    variant: 'default',
    size: 'md',
    as: 'article',
    title: 'Titre de la carte',
    titleAs: 'h3',
    description: 'Description courte qui précise le contenu de la carte.',
    href: undefined,
  },
  render: (args: CspCardProps) => ({
    components: { CspButton, CspCard },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>Contenu principal de la carte, placé dans le slot par défaut.</p>

          <template #footer>
            <CspButton label="Action" variant="primary" />
            <CspButton label="Secondaire" variant="secondary" />
          </template>
        </CspCard>
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspCardProps>

const VARIANTS = ['default', 'alt'] as const
const SIZES = ['sm', 'md', 'lg'] as const

export const Default: Story = {}

export const TitleAndDescription: Story = {
  render: (args: CspCardProps) => ({
    components: { CspCard },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCard v-bind="args" />
      </div>
    `,
  }),
}

export const WithLink: Story = {
  args: {
    title: 'Libellé du lien',
    description: 'Description courte de la carte cliquable.',
    href: '#',
  },
  render: (args: CspCardProps) => ({
    components: { CspCard },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <p>La carte entière est cliquable : titre bleu et flèche signalent l'interactivité.</p>
        </CspCard>
      </div>
    `,
  }),
}

export const WithStartAndEnd: Story = {
  render: (args: CspCardProps) => ({
    components: { CspCard },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCard v-bind="args">
          <template #start>
            <!-- Placeholder : remplacer par de futurs CspTag / CspBadge -->
            <span class="csp-card-story-placeholder">Tag</span>
            <span class="csp-card-story-placeholder">Badge</span>
          </template>

          <p>Corps de la carte décrivant le contenu principal.</p>

          <template #end>
            <!-- Placeholder : informations méta (date, lieu, durée…) -->
            <span>Information méta</span>
          </template>
        </CspCard>
      </div>

      <style>
        .csp-card-story-placeholder {
          display: inline-flex;
          align-items: center;
          padding: 0.125rem 0.5rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          background-color: var(--background-alt-blue-france);
          color: var(--text-action-high-blue-france);
        }
      </style>
    `,
  }),
}

export const Composition: Story = {
  render: (args: CspCardProps) => ({
    components: { CspButton, CspCard },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCard v-bind="args" :title="null" :description="null">
          <template #title>
            Titre via slot
          </template>
          <template #description>
            Description via slot, pouvant contenir du <strong>balisage</strong>.
          </template>

          <p>Corps de la carte libre.</p>

          <template #footer>
            <CspButton label="Libellé" variant="primary" />
          </template>
        </CspCard>
      </div>
    `,
  }),
}

export const Variants: Story = {
  render: (args: CspCardProps) => ({
    components: { CspCard },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="v"
          description="Contenu de démonstration."
        />
      </div>
    `,
  }),
}

export const Sizes: Story = {
  render: (args: CspCardProps) => ({
    components: { CspCard },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex flex-col gap-6 max-w-xl">
        <CspCard
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
          :title="'size: ' + s"
          description="Contenu de démonstration."
        />
      </div>
    `,
  }),
}
