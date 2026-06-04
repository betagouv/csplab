import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'

type CspDialogProps = ComponentPropsAndSlots<typeof CspDialog>

const meta = {
  title: 'Éléments/Génériques/CspDialog',
  component: CspDialog,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['open', 'defaultOpen', 'modal', 'size', 'title', 'description', 'ariaLabel', 'showClose', 'closeLabel'],
    },
    docs: {
      description: {
        component: 'Primitive de dialogue générique, construite sur les primitives `reka-ui` pour la gestion du focus, de la touche Échap et de l\'accessibilité. Utilisez le slot `trigger` pour l\'élément déclencheur et le slot par défaut pour le corps du dialogue.',
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
      description: 'État d\'ouverture initial non contrôlé (utiliser quand `open` n’est pas contrôlé).',
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
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies NonNullable<CspDialogProps['size']>[],
      description: 'Préréglage de la largeur maximale du dialogue.',
      table: {
        type: {
          summary: 'sm | md | lg',
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
      description: 'Label accessible utilisé si aucun titre n\'est fourni.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    showClose: {
      control: { type: 'boolean' },
      description: 'Si vrai, affiche un bouton de fermeture dans l\'en-tête.',
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
      description: 'Label accessible du bouton de fermeture.',
      table: {
        type: {
          summary: 'string',
        },
        defaultValue: {
          summary: 'Close',
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
    size: 'md',
    title: 'Titre du dialogue',
    description: 'Description optionnelle, courte et utile.',
    showClose: true,
    closeLabel: 'Fermer',
  },
  render: (args: CspDialogProps) => ({
    components: { CspButton, CspDialog },
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
      <CspDialog
        v-bind="args"
        :open="args.open === undefined ? undefined : open"
        @update:open="handleUpdateOpen"
      >
        <template #trigger>
          <CspButton
            label="Ouvrir le dialogue"
            variant="primary"
          />
        </template>

        <p class="text-sm">
          Contenu de démonstration. Appuyez sur Échap ou cliquez à l'extérieur pour fermer.
        </p>

        <template #footer>
          <div class="flex gap-3">
            <CspButton
              label="Annuler"
              variant="secondary"
              @click="handleUpdateOpen(false)"
            />
            <CspButton
              label="Confirmer"
              variant="primary"
              @click="handleUpdateOpen(false)"
            />
          </div>
        </template>
      </CspDialog>
    `,
  }),
}

export default meta
type Story = StoryObj<CspDialogProps>

export const Default: Story = {}

export const Controlled: Story = {
  args: {
    open: false,
  },
}

export const Sizes: Story = {
  render: args => ({
    components: { CspDialog, CspButton },
    setup() {
      const sizes = ['sm', 'md', 'lg'] as const
      return { args, sizes }
    },
    template: `
      <div class="flex flex-row gap-6 flex-wrap">
        <CspDialog
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

          <p class="text-sm">
            Taille : <strong>{{ s }}</strong>
          </p>
        </CspDialog>
      </div>
    `,
  }),
}
