import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'

type CspMetaListProps = ComponentPropsAndSlots<typeof CspMetaList>

const meta = {
  title: 'Éléments/Génériques/CspMetaList',
  component: CspMetaList,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['layout', 'size', 'items'],
    },
    docs: {
      description: {
        component: 'Liste de métadonnées avec icône et texte secondaire',
      },
    },
  },
  argTypes: {
    layout: {
      control: { type: 'radio' },
      options: ['inline', 'stacked'] satisfies NonNullable<CspMetaListProps['layout']>[],
      description: 'Disposition des métadonnées : en ligne avec retour à la ligne, ou en pile verticale.',
      table: {
        type: { summary: 'inline | stacked' },
        defaultValue: { summary: 'inline' },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspMetaListProps['size']>[],
      description: 'Taille de la liste : ajuste la taille de texte, l’espacement et la taille des icônes.',
      table: {
        type: { summary: 'sm | md | lg' },
        defaultValue: { summary: 'md' },
      },
    },
    items: {
      control: { type: 'object' },
      description: 'Liste ordonnée des métadonnées à afficher. Chaque item accepte un label visible, une icône Iconify optionnelle et un préfixe réservé aux lecteurs d’écran.',
      table: {
        type: { summary: 'CspMetaItem[]' },
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
    layout: 'inline',
    size: 'md',
    items: [
      { srLabel: 'Information 1', label: 'Libellé 1', icon: 'ri:calendar-line' },
      { srLabel: 'Information 2', label: 'Libellé 2', icon: 'ri:map-pin-2-line' },
      { srLabel: 'Information 3', label: 'Libellé 3', icon: 'ri:government-line' },
      { srLabel: 'Information 4', label: 'Libellé 4', icon: 'ri:price-tag-3-line' },
    ],
  },
  render: (args: CspMetaListProps) => ({
    components: { CspMetaList },
    setup() {
      return { args }
    },
    template: '<CspMetaList v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<CspMetaListProps>

export const Inline: Story = {}

export const WithoutIcons: Story = {
  name: 'Sans icônes',
  args: {
    items: [
      { icon: undefined, srLabel: 'Date', label: 'Libellé 1' },
      { icon: undefined, srLabel: 'Canal', label: 'Libellé 2' },
      { icon: undefined, srLabel: 'Audience', label: 'Libellé 3' },
    ],
  },
}

export const Sizes: Story = {
  render: args => ({
    components: { CspMetaList },
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
          <CspMetaList v-bind="args" :size="size" />
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const Stacked: Story = {
  name: 'Disposition empilée',
  args: {
    layout: 'stacked',
  },
}
