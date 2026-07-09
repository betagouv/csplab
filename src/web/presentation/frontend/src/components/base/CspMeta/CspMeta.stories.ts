import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspMeta from '@/components/base/CspMeta/CspMeta.vue'

type CspMetaProps = ComponentPropsAndSlots<typeof CspMeta>

const meta = {
  title: 'Éléments/Génériques/CspMeta',
  component: CspMeta,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'icon', 'srLabel', 'size'],
    },
    docs: {
      description: {
        component: 'Affichage de métadonnée unitaire avec icône optionnelle et texte secondaire.',
      },
    },
  },
  argTypes: {
    label: {
      control: { type: 'text' },
      description: 'Texte visible de la métadonnée.',
      table: { type: { summary: 'string' } },
    },
    icon: {
      control: { type: 'text' },
      description: 'Icône Iconify optionnelle affichée avant le texte.',
      table: { type: { summary: 'string' } },
    },
    srLabel: {
      control: { type: 'text' },
      description: 'Préfixe réservé aux lecteurs d’écran. Obligatoire pour fournir le contexte sémantique de la métadonnée.',
      table: { type: { summary: 'string' } },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspMetaProps['size']>[],
      description: 'Taille de la métadonnée : ajuste le texte, l’écart et la taille d’icône.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
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
    label: 'Libellé métadonnée',
    icon: 'ri:calendar-line',
    srLabel: 'Information',
    size: 'md',
  },
  render: (args: CspMetaProps) => ({
    components: { CspMeta },
    setup() {
      return { args }
    },
    template: '<CspMeta v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<CspMetaProps>

export const Default: Story = {}

export const WithoutIcon: Story = {
  name: 'Sans icône',
  args: {
    icon: undefined,
  },
}

export const Sizes: Story = {
  render: args => ({
    components: { CspMeta },
    setup() {
      return {
        args,
        sizes: ['sm', 'md', 'lg'],
      }
    },
    template: `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div v-for="size in sizes" :key="size" style="display: flex; flex-direction: column; gap: 0.5rem;">
          <p style="margin: 0; font-size: 0.75rem; color: var(--text-mention-grey);">{{ size }}</p>
          <CspMeta v-bind="args" :size="size" />
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}
