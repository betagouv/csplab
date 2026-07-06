import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'

type CspCalloutProps = ComponentPropsAndSlots<typeof CspCallout>

const meta = {
  title: 'Éléments/Génériques/CspCallout',
  component: CspCallout,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['variant', 'title', 'description', 'icon', 'showIcon'],
    },
    docs: {
      description: {
        component: 'Encart d\'information pour attirer l\'attention de l\'utilisateur sur un message important.',
      },
    },
  },
  argTypes: {
    variant: {
      control: { type: 'radio' },
      options: ['default', 'info', 'success', 'warning', 'error'] satisfies NonNullable<CspCalloutProps['variant']>[],
      description: 'Variante visuelle du callout.',
      table: {
        type: { summary: 'default | info | success | warning | error' },
        defaultValue: { summary: 'default' },
      },
    },
    title: {
      control: { type: 'text' },
      description: 'Titre du callout (ou slot `title`).',
      table: {
        type: { summary: 'string | null' },
        defaultValue: { summary: 'null' },
      },
    },
    description: {
      control: { type: 'text' },
      description: 'Description du callout (ou slot `description`).',
      table: {
        type: { summary: 'string | null' },
        defaultValue: { summary: 'null' },
      },
    },
    icon: {
      control: { type: 'text' },
      description: 'Icône personnalisée. Doit être une référence d\'icône compatible avec `CspIcon` (ex: "ri:lightbulb-line"). Par défaut, l\'icône dépend de la variante.',
      table: {
        type: { summary: 'string | null' },
        defaultValue: { summary: 'null' },
      },
    },
    showIcon: {
      control: { type: 'boolean' },
      description: 'Affiche ou masque l\'icône.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    default: { control: false, table: { disable: true } },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
    key: { control: false, table: { disable: true } },
    ref: { control: false, table: { disable: true } },
    ref_for: { control: false, table: { disable: true } },
    ref_key: { control: false, table: { disable: true } },
  },
  args: {
    variant: 'default',
    title: 'Titre du callout',
    description: 'Description du callout avec des informations complémentaires.',
    icon: null,
    showIcon: true,
  },
  render: (args: CspCalloutProps) => ({
    components: { CspCallout },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCallout v-bind="args" />
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspCalloutProps>

const VARIANTS = ['default', 'info', 'success', 'warning', 'error'] as const

export const Default: Story = {}

export const TitleOnly: Story = {
  args: {
    title: 'Titre du callout sans description',
    description: null,
  },
}

export const WithRichContent: Story = {
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description avec du contenu riche ci-dessous.',
  },
  render: args => ({
    components: { CspCallout },
    setup() {
      return { args }
    },
    template: `
      <div class="max-w-xl">
        <CspCallout v-bind="args">
          <ul>
            <li>Premier élément de la liste</li>
            <li>Deuxième élément de la liste</li>
            <li>Troisième élément de la liste</li>
          </ul>
        </CspCallout>
      </div>
    `,
  }),
}

export const Variants: Story = {
  render: args => ({
    components: { CspCallout },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex flex-col gap-4 max-w-xl">
        <CspCallout
          v-for="v in variants"
          :key="v"
          v-bind="args"
          :variant="v"
          :title="'Titre du callout (' + v + ')'"
          description="Description du callout avec des informations complémentaires."
        />
      </div>
    `,
  }),
}

export const WithCustomIcon: Story = {
  args: {
    variant: 'info',
    title: 'Titre du callout',
    description: 'Description du callout avec une icône personnalisée.',
    icon: 'ri:lightbulb-line',
  },
}

export const WithoutIcon: Story = {
  args: {
    title: 'Titre du callout',
    description: 'Description du callout sans icône.',
    showIcon: false,
  },
}

export const Success: Story = {
  args: {
    variant: 'success',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante success.',
  },
}

export const Warning: Story = {
  args: {
    variant: 'warning',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante warning.',
  },
}

export const Error: Story = {
  args: {
    variant: 'error',
    title: 'Titre du callout',
    description: 'Description du callout avec la variante error.',
  },
}
