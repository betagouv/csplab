import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'

type CspSeparatorProps = ComponentPropsAndSlots<typeof CspSeparator>

const meta = {
  title: 'Éléments/Génériques/CspSeparator',
  component: CspSeparator,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['orientation', 'size', 'variant', 'decorative'],
    },
    docs: {
      description: {
        component: 'Séparateur visuel ou sémantique pour diviser le contenu. Basé sur Reka UI Separator.',
      },
    },
  },
  argTypes: {
    orientation: {
      control: { type: 'radio' },
      options: ['horizontal', 'vertical'] satisfies NonNullable<CspSeparatorProps['orientation']>[],
      description: 'Orientation du séparateur.',
      table: {
        type: {
          summary: 'horizontal | vertical',
        },
        defaultValue: {
          summary: 'horizontal',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspSeparatorProps['size']>[],
      description: 'Taille (épaisseur) du séparateur.',
      table: {
        type: {
          summary: 'sm | md | lg',
        },
        defaultValue: {
          summary: 'md',
        },
      },
    },
    variant: {
      control: { type: 'radio' },
      options: ['default', 'subtle', 'strong'] satisfies NonNullable<CspSeparatorProps['variant']>[],
      description: 'Variante visuelle du séparateur.',
      table: {
        type: {
          summary: 'default | subtle | strong',
        },
        defaultValue: {
          summary: 'default',
        },
      },
    },
    decorative: {
      control: { type: 'boolean' },
      description: 'Si activé, le séparateur est purement décoratif et retiré de l\'arbre d\'accessibilité.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    class: {
      control: false,
      table: {
        disable: true,
      },
    },
    style: {
      control: false,
      table: {
        disable: true,
      },
    },
    key: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref_for: {
      control: false,
      table: {
        disable: true,
      },
    },
    ref_key: {
      control: false,
      table: {
        disable: true,
      },
    },
  },
  args: {
    orientation: 'horizontal',
    size: 'md',
    variant: 'default',
    decorative: false,
  },
  render: (args: CspSeparatorProps) => ({
    components: { CspSeparator },
    setup() {
      return { args }
    },
    template: '<CspSeparator v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<typeof meta>

const VARIANTS = ['default', 'subtle', 'strong'] as const
const SIZES = ['sm', 'md', 'lg'] as const

export const Default: Story = {
  args: {
    orientation: 'horizontal',
  },
}

export const Horizontal: Story = {
  render: args => ({
    components: { CspSeparator },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="v in variants" :key="v">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="horizontal" />
        </div>
      </div>
    `,
  }),
}

export const Vertical: Story = {
  render: args => ({
    components: { CspSeparator },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex gap-8 h-24">
        <div v-for="v in variants" :key="v" class="flex flex-col items-center">
          <p class="mb-2 text-sm text-grey-600">{{ v }}</p>
          <CspSeparator v-bind="args" :variant="v" orientation="vertical" class="h-full" />
        </div>
      </div>
    `,
  }),
}

export const Sizes: Story = {
  render: args => ({
    components: { CspSeparator },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex flex-col gap-8 w-full max-w-md">
        <div v-for="s in sizes" :key="s">
          <p class="mb-2 text-sm text-grey-600">{{ s }}</p>
          <CspSeparator v-bind="args" :size="s" orientation="horizontal" />
        </div>
      </div>
    `,
  }),
}

export const InContext: Story = {
  render: () => ({
    components: { CspSeparator },
    template: `
      <div class="w-full max-w-md">
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 1</h3>
          <p class="text-sm text-grey-600">Contenu de la première section.</p>
        </div>
        <CspSeparator />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 2</h3>
          <p class="text-sm text-grey-600">Contenu de la deuxième section.</p>
        </div>
        <CspSeparator variant="subtle" />
        <div class="p-4">
          <h3 class="font-semibold mb-2">Section 3</h3>
          <p class="text-sm text-grey-600">Contenu de la troisième section.</p>
        </div>
      </div>
    `,
  }),
}

export const VerticalInContext: Story = {
  render: () => ({
    components: { CspSeparator },
    template: `
      <div class="flex items-center gap-4 h-8">
        <span class="text-sm">Élément 1</span>
        <CspSeparator orientation="vertical" class="h-full" />
        <span class="text-sm">Élément 2</span>
        <CspSeparator orientation="vertical" variant="subtle" class="h-full" />
        <span class="text-sm">Élément 3</span>
      </div>
    `,
  }),
}
