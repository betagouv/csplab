import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

type CspIconProps = ComponentPropsAndSlots<typeof CspIcon>

const meta = {
  title: 'Éléments/Génériques/CspIcon',
  component: CspIcon,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['name', 'size'],
    },
    docs: {
      description: {
        component: 'Wrapper générique d\'icône Iconify. La couleur de l\'icône hérite de `currentColor` (stylez-la via CSS sur le parent ou sur l\'icône elle-même).',
      },
    },
  },
  argTypes: {
    name: {
      control: { type: 'text' },
      description: 'Nom de l\'icône Iconify.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    size: {
      control: { type: 'text' },
      description: 'Taille de l\'icône. Accepte un nombre (pixels) ou n\'importe quelle taille CSS valide.',
      table: {
        type: {
          summary: 'number | string',
        },
        defaultValue: {
          summary: '16',
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
    name: 'ri:add-line',
    size: 16,
  },
  render: (args: CspIconProps) => ({
    components: { CspIcon },
    setup() {
      return { args }
    },
    template: '<CspIcon v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<CspIconProps>

export const Default: Story = {
  args: { name: 'ri:add-line', size: 24 },
}

export const Sizes: Story = {
  render: () => ({
    components: { CspIcon },
    setup() {
      return { sizes: [12, 16, 20, 24, 32] }
    },
    template: `
      <div class="flex gap-12 items-end">
        <div v-for="s in sizes" :key="s" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="s" />
          <span>{{ s }}px</span>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const Colors: Story = {
  render: () => ({
    components: { CspIcon },
    setup() {
      return {
        colors: [
          { label: 'Bleu France', value: 'var(--text-action-high-blue-france)' },
          { label: 'Succès', value: 'var(--text-default-success)' },
          { label: 'Erreur', value: 'var(--text-default-error)' },
        ],
      }
    },
    template: `
      <div class="flex gap-12 items-end">
        <div v-for="c in colors" :key="c.label" class="flex flex-col items-center gap-2">
          <CspIcon name="ri:add-line" :size="24" :style="{ color: c.value }" />
          <span :style="{ color: c.value }">{{ c.label }}</span>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

const SAMPLE_ICONS = [
  'ri:add-line',
  'ri:close-line',
  'ri:check-line',
  'ri:search-line',
  'ri:user-line',
  'ri:mail-line',
  'ri:calendar-line',
  'ri:edit-line',
  'ri:delete-bin-line',
  'ri:more-2-fill',
  'ri:arrow-right-line',
  'ri:settings-3-line',
  'ri:notification-3-line',
  'ri:eye-line',
  'ri:price-tag-3-line',
] as const

export const Sample: Story = {
  render: () => ({
    components: { CspIcon },
    setup() {
      return { icons: SAMPLE_ICONS }
    },
    template: `
      <div class="grid grid-cols-5 gap-4">
        <div
          v-for="icon in icons"
          :key="icon"
          class="flex flex-col items-center gap-2 p-3 rounded"
          :style="{ border: '1px solid var(--border-default-grey)' }"
        >
          <CspIcon :name="icon" :size="24" />
          <code class="text-xs">{{ icon }}</code>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}
