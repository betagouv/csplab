import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

type CspBadgeProps = ComponentPropsAndSlots<typeof CspBadge>

const meta = {
  title: 'Éléments/Génériques/CspBadge',
  component: CspBadge,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['variant', 'size', 'label', 'type', 'icon', 'color'],
    },
    docs: {
      description: {
        component: 'Badge générique pour afficher des statuts ou états',
      },
    },
  },
  argTypes: {
    variant: {
      control: { type: 'radio' },
      options: ['default', 'soft', 'outline'] satisfies NonNullable<CspBadgeProps['variant']>[],
      description: 'Variant de style du badge.',
      table: {
        type: {
          summary: 'default | soft | outline',
        },
        defaultValue: {
          summary: 'default',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspBadgeProps['size']>[],
      description: 'Taille du badge.',
      table: {
        type: {
          summary: 'sm | md | lg',
        },
        defaultValue: {
          summary: 'md',
        },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Texte visible à l\'intérieur du badge.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    type: {
      control: { type: 'radio' },
      options: ['info', 'success', 'new', 'warning', 'error'] satisfies NonNullable<CspBadgeProps['type']>[],
      description: 'Type de badge préconfiguré avec des couleurs et icônes par défaut. Ne peut pas être utilisé conjointement avec les props `icon` ou `color`.',
      table: {
        type: {
          summary: 'info | success | new | warning | error',
        },
      },
    },
    icon: {
      control: { type: 'text' },
      description: 'Icone personnalisée à afficher à côté du label. Doit être une référence d\'icône compatible avec le composant `CspIcon` (ex: "ri:settings-3-line"). Ne peut pas être utilisé conjointement avec les props `type` ou `color`.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    color: {
      control: { type: 'text' },
      description: 'Couleur personnalisée pour le badge. Peut être n\'importe quelle valeur de couleur CSS valide (ex: "red", "#ff0000", "rgb(255, 0, 0)"). Ne peut pas être utilisé conjointement avec la prop `type`.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    default: {
      control: false,
      table: {
        disable: true,
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
    variant: 'default',
    size: 'md',
    label: 'Libellé badge',
  },
  render: (args: CspBadgeProps) => ({
    components: { CspBadge },
    setup() {
      return { args }
    },
    template: '<CspBadge v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<typeof meta>

const VARIANTS = [
  'default',
  'soft',
  'outline',
]

const SIZES = [
  'sm',
  'md',
  'lg',
]

const TYPES = [
  'info',
  'success',
  'new',
  'warning',
  'error',

]

export const Default: Story = {
  args: {
    label: 'Libellé badge',
  },
}

export const Variants: Story = {
  render: args => ({
    components: { CspBadge },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex gap-12 flex-wrap">
      <div
        v-for="v in variants"
        :key="v"
      >
        <p class="mb-2">{{ v }}</p>
        <CspBadge
          v-bind="args"
          :variant="v"
          label="Libellé badge"
        />
      </div>
      </div>
    `,
  }),
}

export const Sizes: Story = {
  render: args => ({
    components: { CspBadge },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
          />
        </div>
      </div>
    `,
  }),
}

export const CustomIcon: Story = {
  render: args => ({
    components: { CspBadge },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <CspBadge
            v-bind="args"
            :size="s"
            label="Libellé badge"
            icon="ri:settings-3-line"
          />
        </div>
      </div>
    `,
  }),
}

export const CustomColor: Story = {
  render: args => ({
    components: { CspBadge },
    setup() {
      return { variants: VARIANTS, sizes: SIZES, args }
    },
    template: `
      <div class="flex flex-col gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="s in sizes"
              :key="s"
              v-bind="args"
              :variant="v"
              :size="s"
              label="Libellé badge"
              color="purple"
            />
          </div>
        </div>
      </div>
    `,
  }),
}

export const WithType: Story = {
  render: args => ({
    components: { CspBadge },
    setup() {
      return { variants: VARIANTS, types: TYPES, args }
    },
    template: `
      <div class="flex gap-12 flex-wrap">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <div class="flex gap-8 flex-wrap">
            <CspBadge
              v-for="t in types"
              :key="t"
              v-bind="args"
              :variant="v"
              :type="t"
              label="Libellé badge"
            />
          </div>
        </div>
      </div>
    `,
  }),
}
