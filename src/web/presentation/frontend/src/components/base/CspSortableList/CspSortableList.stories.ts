import type { StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'

interface DemoItem {
  id: string
  label: string
}

interface StoryArgs {
  showPosition: boolean
  showAccessibilityButtons: boolean
}

const meta = {
  title: 'Éléments/Génériques/CspSortableList',
  component: CspSortableList,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['showPosition', 'showAccessibilityButtons'],
    },
  },
  argTypes: {
    showPosition: {
      control: { type: 'boolean' },
      description: 'Afficher le numéro de position.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    showAccessibilityButtons: {
      control: { type: 'boolean' },
      description: 'Afficher les boutons monter/descendre (accessibilité).',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
  },
  args: {
    showPosition: true,
    showAccessibilityButtons: true,
  },
}

export default meta
type Story = StoryObj<StoryArgs>

const itemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: 'var(--csp-space-3)',
  padding: 'var(--csp-space-3) var(--csp-space-4)',
  borderRadius: '0.25rem',
  boxShadow: 'inset 0 0 0 1px var(--border-default-grey)',
  background: 'var(--background-default-grey)',
}

const handleStyle = {
  display: 'flex',
  cursor: 'grab',
  color: 'var(--text-mention-grey)',
}

const positionStyle = {
  minWidth: '1.5rem',
  color: 'var(--text-mention-grey)',
}

const actionsStyle = {
  display: 'flex',
  gap: 'var(--csp-space-1)',
  minWidth: '4rem',
}

export const Default: Story = {
  render: (args: StoryArgs) => ({
    components: { CspSortableList, CspIcon, CspButton },
    setup() {
      const items = ref<DemoItem[]>([
        { id: '1', label: 'Pré-qualification' },
        { id: '2', label: 'Entretien téléphonique' },
        { id: '3', label: 'Entretien technique' },
        { id: '4', label: 'Entretien RH' },
      ])

      function onReorder(newItems: DemoItem[]) {
        items.value = newItems
      }

      return {
        args,
        items,
        itemStyle,
        handleStyle,
        positionStyle,
        actionsStyle,
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
        <template #item="{ item, position, setHandleRef, isDragging, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span v-if="args.showPosition" :style="positionStyle">{{ position }}</span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    `,
  }),
}

interface LockedDemoItem extends DemoItem {
  locked?: boolean
}

const iconStyle = {
  display: 'flex',
  color: 'var(--text-mention-grey)',
}

export const WithLockedItems: Story = {
  args: {
    showPosition: true,
    showAccessibilityButtons: true,
  },
  render: (args: StoryArgs) => ({
    components: { CspSortableList, CspIcon, CspButton },
    setup() {
      const items = ref<LockedDemoItem[]>([
        { id: '1', label: 'Candidature reçue', locked: true },
        { id: '2', label: 'Pré-qualification' },
        { id: '3', label: 'Entretien' },
        { id: '4', label: 'Entretien RH' },
        { id: '5', label: 'Offre clôturée', locked: true },
      ])

      function onReorder(newItems: LockedDemoItem[]) {
        items.value = newItems
      }

      return {
        args,
        items,
        itemStyle,
        iconStyle,
        positionStyle,
        actionsStyle,
        getItemKey: (item: LockedDemoItem) => item.id,
        getItemLabel: (item: LockedDemoItem) => item.label,
        isItemDraggable: (item: LockedDemoItem) => !item.locked,
        onReorder,
      }
    },
    template: `
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        @reorder="onReorder"
      >
        <template #item="{ item, position, setHandleRef, isDragging, isDraggable, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span
              v-if="isDraggable"
              :ref="setHandleRef"
              :style="{ ...iconStyle, cursor: 'grab' }"
            >
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span v-if="args.showPosition" :style="positionStyle">{{ position }}</span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="isDraggable && args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    `,
  }),
}
