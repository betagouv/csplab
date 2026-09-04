import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspToast from '@/components/base/CspToast/CspToast.vue'
import CspToastProvider from '@/components/base/CspToast/CspToastProvider.vue'

type CspToastProps = ComponentPropsAndSlots<typeof CspToast>

const meta = {
  title: 'Éléments/Génériques/CspToast',
  component: CspToast,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: [
        'open',
        'defaultOpen',
        'title',
        'description',
        'duration',
        'variant',
        'showIcon',
        'actionLabel',
        'actionAltText',
        'showClose',
        'closeLabel',
      ],
    },
    docs: {
      description: {
        component: 'Notification toast accessible basée sur reka-ui. Doit être utilisé à l\'intérieur d\'un unique CspToastProvider placé à la racine de l\'app.',
      },
    },
  },
  argTypes: {
    open: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture contrôlé. Liez avec `v-model:open`.',
      table: {
        type: { summary: 'boolean' },
      },
    },
    defaultOpen: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture initial en mode non contrôlé.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    title: {
      control: { type: 'text' },
      description: 'Titre du toast (ou slot `title`).',
      table: {
        type: { summary: 'string | null' },
      },
    },
    description: {
      control: { type: 'text' },
      description: 'Description du toast (ou slot `description`).',
      table: {
        type: { summary: 'string | null' },
      },
    },
    duration: {
      control: { type: 'number' },
      description: 'Durée d\'affichage en millisecondes. Hérite du provider si non défini.',
      table: {
        type: { summary: 'number' },
      },
    },
    variant: {
      control: { type: 'radio' },
      options: ['default', 'info', 'success', 'warning', 'error'] satisfies NonNullable<CspToastProps['variant']>[],
      description: 'Variante visuelle de la notification.',
      table: {
        type: { summary: 'default | info | success | warning | error' },
        defaultValue: { summary: 'default' },
      },
    },
    showIcon: {
      control: { type: 'boolean' },
      description: 'Affiche ou masque l\'icone.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    actionLabel: {
      control: { type: 'text' },
      description: 'Label du bouton d\'action.',
      table: {
        type: { summary: 'string | null' },
      },
    },
    actionAltText: {
      control: { type: 'text' },
      description: 'Texte alternatif annoncé pour l\'action.',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'Exécuter l\'action' },
      },
    },
    showClose: {
      control: { type: 'boolean' },
      description: 'Affiche ou masque le bouton de fermeture.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    closeLabel: {
      control: { type: 'text' },
      description: 'Libellé accessible du bouton de fermeture.',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'Fermer la notification' },
      },
    },
    class: {
      control: false,
      table: { disable: true },
    },
    style: {
      control: false,
      table: { disable: true },
    },
    key: {
      control: false,
      table: { disable: true },
    },
    ref: {
      control: false,
      table: { disable: true },
    },
    ref_for: {
      control: false,
      table: { disable: true },
    },
    ref_key: {
      control: false,
      table: { disable: true },
    },
  },
  args: {
    defaultOpen: false,
    title: 'Action terminée',
    description: 'Votre modification a bien été enregistrée.',
    variant: 'success',
    showIcon: true,
    actionLabel: 'Annuler',
    actionAltText: 'Annuler la dernière action',
    showClose: true,
    closeLabel: 'Fermer la notification',
  },
  render: (args: CspToastProps) => ({
    components: { CspButton, CspToast, CspToastProvider },
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

      function showToast() {
        open.value = true
      }

      function handleUpdateOpen(value: boolean) {
        open.value = value
      }

      return { args, open, showToast, handleUpdateOpen }
    },
    template: `
      <CspToastProvider>
        <CspButton
          label="Afficher le toast"
          variant="primary"
          @click="showToast"
        />

        <CspToast
          v-bind="args"
          :open="args.open === undefined ? open : args.open"
          @update:open="handleUpdateOpen"
        />
      </CspToastProvider>
    `,
  }),
}

export default meta
type Story = StoryObj<CspToastProps>

export const Default: Story = {}

export const Variants: Story = {
  render: args => ({
    components: { CspButton, CspToast, CspToastProvider },
    setup() {
      const variants = ['default', 'info', 'success', 'warning', 'error'] as const
      const open = ref(false)
      const currentVariant = ref<(typeof variants)[number]>('default')

      function openVariant(variant: (typeof variants)[number]) {
        currentVariant.value = variant
        open.value = true
      }

      function updateOpen(value: boolean) {
        open.value = value
      }

      return { args, variants, open, currentVariant, openVariant, updateOpen }
    },
    template: `
      <CspToastProvider>
        <div class="flex flex-wrap gap-3">
          <CspButton
            v-for="variant in variants"
            :key="variant"
            :label="'Toast ' + variant"
            variant="secondary"
            @click="openVariant(variant)"
          />
        </div>

        <CspToast
          v-bind="args"
          :open="open"
          :variant="currentVariant"
          :title="'Notification ' + currentVariant"
          :description="'Exemple pour la variante ' + currentVariant + '.'"
          @update:open="updateOpen"
        />
      </CspToastProvider>
    `,
  }),
}

export const MultipleToasts: Story = {
  render: () => ({
    components: { CspButton, CspToast, CspToastProvider },
    setup() {
      const toasts = ref<Array<{ id: number, variant: 'info' | 'success' | 'warning' | 'error', title: string }>>([])
      let nextId = 0

      function addToast(variant: 'info' | 'success' | 'warning' | 'error') {
        toasts.value.push({
          id: nextId++,
          variant,
          title: `Notification ${variant} #${nextId}`,
        })
      }

      function removeToast(id: number) {
        toasts.value = toasts.value.filter(t => t.id !== id)
      }

      return { toasts, addToast, removeToast }
    },
    template: `
      <CspToastProvider :duration="4000">
        <div class="flex flex-wrap gap-3">
          <CspButton label="Info" variant="secondary" @click="addToast('info')" />
          <CspButton label="Success" variant="secondary" @click="addToast('success')" />
          <CspButton label="Warning" variant="secondary" @click="addToast('warning')" />
          <CspButton label="Error" variant="secondary" @click="addToast('error')" />
        </div>

        <CspToast
          v-for="toast in toasts"
          :key="toast.id"
          :open="true"
          :variant="toast.variant"
          :title="toast.title"
          description="Cette notification fonctionne avec les autres."
          :show-close="true"
          @update:open="(v) => !v && removeToast(toast.id)"
        />
      </CspToastProvider>
    `,
  }),
}
