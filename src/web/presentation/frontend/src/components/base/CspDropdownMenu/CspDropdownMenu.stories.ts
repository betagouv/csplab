import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import {
  CspDropdownMenu,
  CspDropdownMenuGroup,
  CspDropdownMenuItem,
  CspDropdownMenuLabel,
  CspDropdownMenuSeparator,
} from '@/components/base/CspDropdownMenu'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

type CspDropdownMenuProps = ComponentPropsAndSlots<typeof CspDropdownMenu>

const meta = {
  title: 'Éléments/Génériques/CspDropdownMenu',
  component: CspDropdownMenu,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['align', 'side', 'sideOffset'],
    },
    docs: {
      description: {
        component: 'Menu déroulant accessible basé sur les primitives `reka-ui`. Utilisez le slot `trigger` pour l\'élément déclencheur et le slot par défaut pour les items du menu.',
      },
    },
  },
  argTypes: {
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
    align: 'start',
    side: 'bottom',
    sideOffset: 8,
  },
  render: (args: CspDropdownMenuProps) => ({
    components: {
      CspDropdownMenu,
      CspDropdownMenuItem,
      CspDropdownMenuSeparator,
      CspButton,
      CspIcon,
    },
    setup() {
      return { args }
    },
    template: `
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Ouvrir le menu" variant="secondary" />
          </template>

          <CspDropdownMenuItem>
            <CspIcon name="ri:user-line" :size="16" />
            Mon profil
          </CspDropdownMenuItem>
          <CspDropdownMenuItem>
            <CspIcon name="ri:settings-3-line" :size="16" />
            Paramètres
          </CspDropdownMenuItem>
          <CspDropdownMenuSeparator />
          <CspDropdownMenuItem>
            <CspIcon name="ri:logout-box-r-line" :size="16" />
            Se déconnecter
          </CspDropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspDropdownMenuProps>

const SIDES = ['top', 'right', 'bottom', 'left'] as const
const ALIGNS = ['start', 'center', 'end'] as const

export const Default: Story = {}

export const Positions: Story = {
  render: args => ({
    components: {
      CspDropdownMenu,
      CspDropdownMenuItem,
      CspButton,
    },
    setup() {
      return { sides: SIDES, args }
    },
    template: `
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <CspDropdownMenu
          v-for="side in sides"
          :key="side"
          v-bind="args"
          :side="side"
        >
          <template #trigger>
            <CspButton :label="side" variant="secondary" />
          </template>

          <CspDropdownMenuItem>Option 1</CspDropdownMenuItem>
          <CspDropdownMenuItem>Option 2</CspDropdownMenuItem>
          <CspDropdownMenuItem>Option 3</CspDropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const Alignments: Story = {
  render: args => ({
    components: {
      CspDropdownMenu,
      CspDropdownMenuItem,
      CspButton,
    },
    setup() {
      return { aligns: ALIGNS, args }
    },
    template: `
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <CspDropdownMenu
          v-for="align in aligns"
          :key="align"
          v-bind="args"
          side="bottom"
          :align="align"
        >
          <template #trigger>
            <CspButton :label="align" variant="tertiary" />
          </template>

          <CspDropdownMenuItem>Option 1</CspDropdownMenuItem>
          <CspDropdownMenuItem>Option 2</CspDropdownMenuItem>
          <CspDropdownMenuItem>Option 3</CspDropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const WithLabelsAndGroups: Story = {
  render: args => ({
    components: {
      CspDropdownMenu,
      CspDropdownMenuGroup,
      CspDropdownMenuItem,
      CspDropdownMenuLabel,
      CspDropdownMenuSeparator,
      CspButton,
      CspIcon,
    },
    setup() {
      return { args }
    },
    template: `
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Menu avec groupes" variant="secondary" />
          </template>

          <CspDropdownMenuLabel>Mon compte</CspDropdownMenuLabel>
          <CspDropdownMenuGroup>
            <CspDropdownMenuItem>
              <CspIcon name="ri:user-line" :size="16" />
              Profil
            </CspDropdownMenuItem>
            <CspDropdownMenuItem>
              <CspIcon name="ri:settings-3-line" :size="16" />
              Paramètres
            </CspDropdownMenuItem>
          </CspDropdownMenuGroup>

          <CspDropdownMenuSeparator />

          <CspDropdownMenuLabel>Équipe</CspDropdownMenuLabel>
          <CspDropdownMenuGroup>
            <CspDropdownMenuItem>
              <CspIcon name="ri:group-line" :size="16" />
              Membres
            </CspDropdownMenuItem>
            <CspDropdownMenuItem>
              <CspIcon name="ri:add-line" :size="16" />
              Inviter
            </CspDropdownMenuItem>
          </CspDropdownMenuGroup>

          <CspDropdownMenuSeparator />

          <CspDropdownMenuItem>
            <CspIcon name="ri:logout-box-r-line" :size="16" />
            Se déconnecter
          </CspDropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `,
  }),
}

export const WithIcons: Story = {
  render: args => ({
    components: {
      CspDropdownMenu,
      CspDropdownMenuItem,
      CspDropdownMenuSeparator,
      CspButton,
      CspIcon,
    },
    setup() {
      return { args }
    },
    template: `
      <div class="flex justify-center p-16">
        <CspDropdownMenu v-bind="args">
          <template #trigger>
            <CspButton label="Actions" variant="primary" />
          </template>

          <CspDropdownMenuItem>
            <CspIcon name="ri:edit-line" :size="16" />
            Modifier
          </CspDropdownMenuItem>
          <CspDropdownMenuItem>
            <CspIcon name="ri:eye-line" :size="16" />
            Aperçu
          </CspDropdownMenuItem>
          <CspDropdownMenuItem>
            <CspIcon name="ri:external-link-line" :size="16" />
            Ouvrir dans un nouvel onglet
          </CspDropdownMenuItem>
          <CspDropdownMenuSeparator />
          <CspDropdownMenuItem>
            <CspIcon name="ri:delete-bin-line" :size="16" />
            Supprimer
          </CspDropdownMenuItem>
        </CspDropdownMenu>
      </div>
    `,
  }),
}
