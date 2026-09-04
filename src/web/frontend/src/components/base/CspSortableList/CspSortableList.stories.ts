import type { StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'

interface DemoItem {
  id: string
  label: string
}

const meta = {
  title: 'Éléments/Génériques/CspSortableList',
  component: CspSortableList,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Liste réordonnable par drag and drop. Accessible via les fonctions `moveUp`/`moveDown` exposées dans le slot.',
      },
    },
  },
  argTypes: {
    items: {
      control: false,
      description: 'Liste des éléments à afficher.',
      table: {
        type: { summary: 'T[]' },
      },
    },
    getItemKey: {
      control: false,
      description: 'Fonction retournant la clé unique de chaque élément.',
      table: {
        type: { summary: '(item: T) => string' },
      },
    },
    getItemLabel: {
      control: false,
      description: 'Fonction retournant le libellé pour les annonces d\'accessibilité.',
      table: {
        type: { summary: '(item: T) => string' },
      },
    },
    isItemDraggable: {
      control: false,
      description: 'Fonction déterminant si un élément est déplaçable.',
      table: {
        type: { summary: '(item: T, index: number) => boolean' },
        defaultValue: { summary: '() => true' },
      },
    },
    getItemVariant: {
      control: false,
      description: 'Fonction retournant la variante visuelle de chaque élément.',
      table: {
        type: { summary: '(item: T, index: number) => \'default\' | \'alt\'' },
        defaultValue: { summary: '() => \'default\'' },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive le drag and drop sur toute la liste.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' },
      },
    },
    onReorder: {
      action: 'reorder',
      description: 'Émis quand la liste est réordonnée.',
      table: {
        category: 'Events',
        type: { summary: '(items: T[]) => void' },
      },
    },
    item: {
      control: false,
      description: 'Slot pour personnaliser le contenu de chaque élément. Expose : `item`, `index`, `isDragging`, `isDraggable`, `canMoveUp`, `canMoveDown`, `moveUp`, `moveDown`.',
      table: {
        category: 'Slots',
        type: { summary: 'slot' },
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
}

export default meta
type Story = StoryObj

export const Default: Story = {
  render: () => ({
    components: { CspSortableList },
    setup() {
      const items = ref<DemoItem[]>([
        { id: '1', label: 'Élément 1' },
        { id: '2', label: 'Élément 2' },
        { id: '3', label: 'Élément 3' },
        { id: '4', label: 'Élément 4' },
      ])

      function onReorder(newItems: DemoItem[]) {
        items.value = newItems
      }

      return {
        items,
        getItemKey: (item: DemoItem) => item.id,
        getItemLabel: (item: DemoItem) => item.label,
        onReorder,
      }
    },
    template: `
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    `,
  }),
}

interface PinnedDemoItem extends DemoItem {
  pinned?: boolean
}

export const WithPinnedItems: Story = {
  render: () => ({
    components: { CspSortableList },
    setup() {
      const items = ref<PinnedDemoItem[]>([
        { id: '1', label: 'Élément épinglé', pinned: true },
        { id: '2', label: 'Élément 2' },
        { id: '3', label: 'Élément 3' },
        { id: '4', label: 'Élément 4' },
        { id: '5', label: 'Élément 5' },
      ])

      function onReorder(newItems: PinnedDemoItem[]) {
        const pinnedIndex = newItems.findIndex(item => item.pinned)
        if (pinnedIndex !== 0)
          return

        items.value = newItems
      }

      return {
        items,
        getItemKey: (item: PinnedDemoItem) => item.id,
        getItemLabel: (item: PinnedDemoItem) => item.label,
        isItemDraggable: (item: PinnedDemoItem) => !item.pinned,
        getItemVariant: (item: PinnedDemoItem) => item.pinned ? 'alt' : 'default',
        onReorder,
      }
    },
    template: `
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        :get-item-variant="getItemVariant"
        @reorder="onReorder"
      >
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    `,
  }),
}

export const WithActions: Story = {
  render: () => ({
    components: { CspSortableList, CspButton, CspDropdownMenu },
    setup() {
      const items = ref<DemoItem[]>([
        { id: '1', label: 'Élément 1' },
        { id: '2', label: 'Élément 2' },
        { id: '3', label: 'Élément 3' },
        { id: '4', label: 'Élément 4' },
      ])

      function onReorder(newItems: DemoItem[]) {
        items.value = newItems
      }

      function removeItem(id: string) {
        items.value = items.value.filter(item => item.id !== id)
      }

      function getMenuSections(canMoveUp: boolean, canMoveDown: boolean, moveUp: () => void, moveDown: () => void, itemId: string) {
        return [
          {
            items: [
              { label: 'Monter', icon: 'ri:arrow-up-s-line', disabled: !canMoveUp, onSelect: moveUp },
              { label: 'Descendre', icon: 'ri:arrow-down-s-line', disabled: !canMoveDown, onSelect: moveDown },
            ],
          },
          {
            items: [
              { label: 'Supprimer', icon: 'ri:delete-bin-line', destructive: true, onSelect: () => removeItem(itemId) },
            ],
          },
        ]
      }

      return {
        items,
        getItemKey: (item: DemoItem) => item.id,
        getItemLabel: (item: DemoItem) => item.label,
        onReorder,
        getMenuSections,
      }
    },
    template: `
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, canMoveUp, canMoveDown, moveUp, moveDown }">
          <span style="flex: 1;">{{ item.label }}</span>
          <CspDropdownMenu
            :sections="getMenuSections(canMoveUp, canMoveDown, moveUp, moveDown, item.id)"
            side="bottom"
            align="end"
          >
            <template #trigger>
              <CspButton
                icon="ri:more-2-fill"
                variant="tertiary-no-outline"
                size="sm"
                aria-label="Actions"
              />
            </template>
          </CspDropdownMenu>
        </template>
      </CspSortableList>
    `,
  }),
}
