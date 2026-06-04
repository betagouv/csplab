import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'

type CspAvatarProps = ComponentPropsAndSlots<typeof CspAvatar>

const meta = {
  title: 'Éléments/Génériques/CspAvatar',
  component: CspAvatar,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['name', 'size'],
    },
    docs: {
      description: {
        component: 'Avatar générique affichant les initiales dérivées du nom fourni. Affiche `?` quand aucun nom n\'est donné.',
      },
    },
  },
  argTypes: {
    name: {
      control: { type: 'text' },
      description: 'Nom complet utilisé pour générer les initiales et comme aria-label accessible.',
      table: {
        type: { summary: 'string' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspAvatarProps['size']>[],
      description: 'Taille de l\'csp-avatar.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
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
    name: 'Marie Curie',
    size: 'md',
  },
  render: (args: CspAvatarProps) => ({
    components: { CspAvatar },
    setup() {
      return { args }
    },
    template: '<CspAvatar v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<CspAvatarProps>

export const Default: Story = {}

export const SingleWordName: Story = {
  args: { name: 'Camille' },
}

export const Anonymous: Story = {
  args: { name: null },
}

export const Sizes: Story = {
  render: args => ({
    components: { CspAvatar },
    setup() {
      return { sizes: ['sm', 'md', 'lg'] as const, args }
    },
    template: `
      <div class="flex items-end gap-8">
        <div
          v-for="s in sizes"
          :key="s"
          class="flex flex-col items-center gap-2"
        >
          <CspAvatar v-bind="args" :size="s" />
          <p class="text-sm">{{ s }}</p>
        </div>
      </div>
    `,
  }),
}
