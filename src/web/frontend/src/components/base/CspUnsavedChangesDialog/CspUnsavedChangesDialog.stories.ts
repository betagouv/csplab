import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspUnsavedChangesDialog from './CspUnsavedChangesDialog.vue'

const meta = {
  title: 'Éléments/Génériques/CspUnsavedChangesDialog',
  component: CspUnsavedChangesDialog,
  tags: ['autodocs'],
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        component: 'Confirmation demandée avant de quitter une saisie non enregistrée. Émet `keepEditing` sur « Continuer l\'édition », la touche Échap et le clic en dehors, et `leave` sur « Quitter sans enregistrer ». Se pilote avec `useUnsavedChangesGuard`.',
      },
    },
  },
  args: {
    open: false,
  },
  render: () => ({
    components: { CspButton, CspUnsavedChangesDialog },
    setup() {
      const open = ref(false)
      return { open }
    },
    template: `
      <CspButton
        label="Quitter la saisie"
        variant="primary"
        @click="open = true"
      />
      <CspUnsavedChangesDialog
        :open="open"
        @keep-editing="open = false"
        @leave="open = false"
      />
    `,
  }),
} satisfies Meta<typeof CspUnsavedChangesDialog>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}
