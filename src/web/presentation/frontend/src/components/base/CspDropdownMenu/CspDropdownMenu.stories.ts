import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useStoryOpenState } from '@/stories/useStoryOpenState'

type CspDropdownMenuProps = ComponentPropsAndSlots<typeof CspDropdownMenu>

const DEMO_SECTIONS = [
  {
    items: [
      { label: 'Ouvrir', icon: 'ri:external-link-line' },
      { label: 'Renommer', icon: 'ri:pencil-line' },
    ],
  },
  {
    items: [
      { label: 'Dupliquer', icon: 'ri:file-copy-line', disabled: true },
      { label: 'Supprimer', icon: 'ri:delete-bin-line', destructive: true },
    ],
  },
]

const meta = {
  title: 'Éléments/Génériques/CspDropdownMenu',
  component: CspDropdownMenu,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['open', 'align', 'side', 'sideOffset'],
    },
    docs: {
      description: {
        component: 'Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l\'élément déclencheur et le slot par défaut pour les items du menu.',
      },
    },
  },
  argTypes: {
    sections: {
      control: false,
      description: 'Sections d\'items. Chaque section peut contenir plusieurs `{ label, icon?, disabled?, destructive?, onSelect? }`.',
      table: {
        type: { summary: 'CspDropdownMenuSection[]' },
      },
    },
    open: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture contrôlé. Liez avec `v-model:open`.',
      table: {
        type: { summary: 'boolean' },
      },
    },
    align: {
      control: { type: 'radio' },
      options: ['start', 'center', 'end'] satisfies NonNullable<CspDropdownMenuProps['align']>[],
      description: 'Alignement du menu par rapport au déclencheur.',
      table: {
        type: {
          summary: 'start | center | end',
        },
        defaultValue: {
          summary: 'start',
        },
      },
    },
    side: {
      control: { type: 'radio' },
      options: ['top', 'right', 'bottom', 'left'] satisfies NonNullable<CspDropdownMenuProps['side']>[],
      description: 'Position du menu par rapport au déclencheur.',
      table: {
        type: {
          summary: 'top | right | bottom | left',
        },
        defaultValue: {
          summary: 'top',
        },
      },
    },
    sideOffset: {
      control: { type: 'number' },
      description: 'Distance entre le menu et le déclencheur, en pixels.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '8',
        },
      },
    },
    trigger: {
      control: false,
      table: {
        disable: true,
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
    sections: DEMO_SECTIONS,
    align: 'start',
    side: 'bottom',
    sideOffset: 8,
  },
  render: (args: CspDropdownMenuProps) => ({
    components: { CspDropdownMenu, CspButton },
    setup() {
      const { controlledOpen, handleUpdateOpen } = useStoryOpenState(args)

      return { args, controlledOpen, handleUpdateOpen }
    },
    template: `
      <CspDropdownMenu
        v-bind="args"
        :open="controlledOpen"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            icon="ri:more-2-line"
            variant="tertiary"
            label="Ouvrir le menu déroulant"
          />
        </template>
      </CspDropdownMenu>
    `,
  }),
}

export default meta
type Story = StoryObj<CspDropdownMenuProps>

export const Default: Story = {
  name: 'Par défaut',
}

export const Sides: Story = {
  name: 'Côtés',
  render: (args: CspDropdownMenuProps) => ({
    components: { CspDropdownMenu, CspButton },
    setup() {
      const sides = [
        { label: 'Haut', value: 'top' },
        { label: 'Droite', value: 'right' },
        { label: 'Bas', value: 'bottom' },
        { label: 'Gauche', value: 'left' },
      ] satisfies { label: string, value: NonNullable<CspDropdownMenuProps['side']> }[]

      return { sides, args }
    },
    template: `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="s.value"
            :side="s.value"
          >
            <template #trigger>
              <CspButton :label="s.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    `,
  }),
}

export const Alignments: Story = {
  name: 'Alignements',
  render: (args: CspDropdownMenuProps) => ({
    components: { CspDropdownMenu, CspButton },
    setup() {
      const alignments = [
        { label: 'Début', value: 'start' },
        { label: 'Centre', value: 'center' },
        { label: 'Fin', value: 'end' },
      ] satisfies { label: string, value: NonNullable<CspDropdownMenuProps['align']> }[]

      return { alignments, args }
    },
    template: `
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspDropdownMenu
            v-bind="args"
            :key="a.value"
            :align="a.value"
          >
            <template #trigger>
              <CspButton :label="a.label" variant="tertiary" />
            </template>
            <p class="text-sm">Contenu libre du menu déroulant.</p>
          </CspDropdownMenu>
        </div>
      </div>
    `,
  }),
}
