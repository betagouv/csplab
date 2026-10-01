import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspFiltersDrawer from './CspFiltersDrawer.vue'

const meta = {
  title: 'Compositions/Génériques/CspFiltersDrawer',
  component: CspFiltersDrawer,
  tags: ['autodocs'],
  parameters: {
    controls: { disable: true },
    docs: {
      description: {
        component: 'Tiroir de filtres : les champs passés dans le slot par défaut, suivis des boutons « Appliquer les filtres » et « Réinitialiser ». Émet `apply` et `reset` ; `canReset` active la réinitialisation.',
      },
    },
  },
  args: {
    open: false,
    canReset: false,
  },
  render: () => ({
    components: { CspButton, CspCheckboxGroup, CspFiltersDrawer },
    setup() {
      const open = ref(false)
      const statuts = ref<string[]>([])
      const canReset = computed(() => statuts.value.length > 0)
      const options = [
        { value: 'brouillon', label: 'Brouillon' },
        { value: 'publie', label: 'Publié' },
        { value: 'archive', label: 'Archivé' },
      ]
      return { open, statuts, canReset, options }
    },
    template: `
      <CspButton
        label="Filtres"
        variant="tertiary"
        icon="ri:filter-line"
        is-icon-left
        @click="open = true"
      />
      <CspFiltersDrawer
        v-model:open="open"
        :can-reset="canReset"
        @apply="open = false"
        @reset="statuts = []"
      >
        <CspCheckboxGroup
          v-model="statuts"
          label="Statut"
          :options="options"
        />
      </CspFiltersDrawer>
    `,
  }),
} satisfies Meta<typeof CspFiltersDrawer>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}
