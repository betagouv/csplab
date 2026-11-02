import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import { PALETTE_COLORS } from '@/styles/palette'

type CspLabelProps = ComponentPropsAndSlots<typeof CspLabel>

const meta = {
  title: 'Éléments/Génériques/CspLabel',
  component: CspLabel,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'color', 'size', 'bordered', 'clickable'],
    },
    docs: {
      description: {
        component: 'Étiquette de catégorie : fond teinté, texte et pastille d\'une couleur de la palette. Le libellé porte l\'information, la couleur aide au repérage.',
      },
    },
  },
  argTypes: {
    label: {
      control: { type: 'text' },
      description: 'Libellé de l\'étiquette.',
      table: { type: { summary: 'string' } },
    },
    color: {
      control: { type: 'select' },
      options: [...PALETTE_COLORS],
      description: 'Couleur de la palette.',
      table: { type: { summary: 'PaletteColor' }, defaultValue: { summary: 'grey' } },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md'] satisfies NonNullable<CspLabelProps['size']>[],
      description: 'Taille de l\'étiquette.',
      table: { type: { summary: 'sm | md' }, defaultValue: { summary: 'sm' } },
    },
    bordered: {
      control: { type: 'boolean' },
      description: 'Filet de 1 px, de la couleur de la pastille à 26 % d\'opacité.',
      table: { type: { summary: 'boolean' }, defaultValue: { summary: 'true' } },
    },
    clickable: {
      control: { type: 'boolean' },
      description: 'Affiche l\'étiquette comme un bouton, avec ses états de survol, d\'appui et de focus. Quand le libellé seul ne décrit pas l\'action, on donne le nom accessible par `aria-label`.',
      table: { type: { summary: 'boolean' }, defaultValue: { summary: 'false' } },
    },
  },
  args: {
    label: 'Libellé',
    color: 'blue',
    size: 'sm',
    bordered: true,
    clickable: false,
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: 'Par défaut',
}

export const Palette: Story = {
  name: 'Couleurs, avec et sans filet',
  render: () => ({
    components: { CspLabel },
    setup() {
      return { colors: PALETTE_COLORS, sizes: ['sm', 'md'] }
    },
    template: `
      <div class="flex flex-col gap-4">
        <template v-for="size in sizes" :key="size">
          <div v-for="bordered in [true, false]" :key="String(bordered)" class="flex flex-row gap-2 flex-wrap">
            <CspLabel v-for="color in colors" :key="color" :label="color" :color="color" :size="size" :bordered="bordered" />
          </div>
        </template>
      </div>
    `,
  }),
  parameters: { controls: { disable: true } },
}
