import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { DialogClose } from 'reka-ui'
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'

type CspDrawerProps = ComponentPropsAndSlots<typeof CspDrawer>

const meta = {
  title: 'Éléments/Génériques/CspDrawer',
  component: CspDrawer,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['open', 'defaultOpen', 'modal', 'side', 'size', 'title', 'description', 'ariaLabel', 'showClose', 'closeLabel'],
    },
    docs: {
      description: {
        component: 'Tiroir générique (panneau latéral)',
      },
    },
  },
  argTypes: {
    open: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture contrôlé. Liez avec `v-model:open`.',
      table: {
        type: {
          summary: 'boolean',
        },
      },
    },
    defaultOpen: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture initial non contrôlé (utilisez quand `open` n\'est pas contrôlé).',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    modal: {
      control: { type: 'boolean' },
      description: 'Si vrai, capture le focus et désactive les interactions extérieures.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'true',
        },
      },
    },
    side: {
      control: { type: 'radio' },
      options: ['left', 'right'] satisfies NonNullable<CspDrawerProps['side']>[],
      description: 'Côté auquel le tiroir est attaché.',
      table: {
        type: {
          summary: 'left | right',
        },
        defaultValue: {
          summary: 'right',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['xs', 'sm', 'md', 'lg', 'xl', 'full'] satisfies NonNullable<CspDrawerProps['size']>[],
      description: 'Preset de largeur du tiroir.',
      table: {
        type: {
          summary: 'xs | sm | md | lg | xl | full',
        },
        defaultValue: {
          summary: 'md',
        },
      },
    },
    title: {
      control: { type: 'text' },
      description: 'Texte du titre (ou utilisez le slot `title`). Recommandé pour l\'accessibilité.',
      table: {
        type: {
          summary: 'string | null',
        },
      },
    },
    description: {
      control: { type: 'text' },
      description: 'Texte de description (ou utilisez le slot `description`).',
      table: {
        type: {
          summary: 'string | null',
        },
      },
    },
    ariaLabel: {
      control: { type: 'text' },
      description: 'Libellé accessible utilisé lorsqu\'aucun titre n\'est fourni.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    showClose: {
      control: { type: 'boolean' },
      description: 'Indique s\'il faut afficher un bouton de fermeture dans l\'en-tête.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'true',
        },
      },
    },
    closeLabel: {
      control: { type: 'text' },
      description: 'Libellé accessible du bouton de fermeture.',
      table: {
        type: {
          summary: 'string',
        },
        defaultValue: {
          summary: 'Fermer',
        },
      },
    },
    trigger: {
      control: false,
      table: {
        disable: true,
      },
    },
    footer: {
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
    defaultOpen: false,
    modal: true,
    side: 'right',
    size: 'md',
    title: 'Titre du tiroir',
    description: 'Informations complémentaires sur ce panneau.',
    showClose: true,
    closeLabel: 'Fermer',
  },
  render: (args: CspDrawerProps) => ({
    components: { CspButton, CspDrawer, DialogClose },
    setup() {
      const open = ref(Boolean(args.open))

      watch(
        () => args.open,
        (value) => {
          if (value === undefined) {
            return
          }

          open.value = value
        },
      )

      function handleUpdateOpen(value: boolean) {
        open.value = value
      }

      return { args, open, handleUpdateOpen }
    },
    template: `
      <CspDrawer
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le tiroir"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu principal du tiroir, placé dans le slot par défaut
        </p>

        <div class="h-48" />

        <template #footer>
          <div class="flex gap-3">
            <DialogClose as-child>
              <CspButton
                label="Fermer"
                variant="secondary"
              />
            </DialogClose>
          </div>
        </template>
      </CspDrawer>
    `,
  }),
}

export default meta
type Story = StoryObj<CspDrawerProps>

export const Default: Story = {}

export const Controlled: Story = {
  args: {
    open: false,
  },
}

export const Sides: Story = {
  render: args => ({
    components: { CspDrawer, CspButton },
    setup() {
      const sides = ['left', 'right'] as const
      return { args, sides }
    },
    template: `
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sides"
          :key="s"
          v-bind="args"
          :side="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Side: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `,
  }),
}

export const Sizes: Story = {
  render: args => ({
    components: { CspDrawer, CspButton },
    setup() {
      const sizes = ['xs', 'sm', 'md', 'lg', 'xl', 'full'] as const
      return { args, sizes }
    },
    template: `
      <div class="flex gap-6 flex-wrap">
        <CspDrawer
          v-for="s in sizes"
          :key="s"
          v-bind="args"
          :size="s"
        >
          <template #trigger>
            <CspButton
              :label="'Ouvrir (' + s + ')'"
              variant="secondary"
            />
          </template>

          <p class="text-sm">Size: <strong>{{ s }}</strong></p>
        </CspDrawer>
      </div>
    `,
  }),
}
