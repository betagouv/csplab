import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import { useStoryOpenState } from '@/stories/useStoryOpenState'

type CspPopoverProps = ComponentPropsAndSlots<typeof CspPopover>

const meta = {
  title: 'Éléments/Génériques/CspPopover',
  component: CspPopover,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['open', 'side', 'align'],
    },
    docs: {
      description: {
        component: 'Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre.',
      },
    },
    layout: 'centered',
  },
  argTypes: {
    open: {
      control: { type: 'boolean' },
      description: 'État d\'ouverture contrôlé. Liez avec `v-model:open`.',
      table: {
        type: { summary: 'boolean' },
      },
    },
    side: {
      control: { type: 'radio' },
      options: ['top', 'right', 'bottom', 'left'] satisfies NonNullable<CspPopoverProps['side']>[],
      description: 'Côté d\'apparition du popover.',
      table: {
        type: { summary: 'top | right | bottom | left' },
        defaultValue: { summary: 'bottom' },
      },
    },
    align: {
      control: { type: 'radio' },
      options: ['start', 'center', 'end'] satisfies NonNullable<CspPopoverProps['align']>[],
      description: 'Alignement du popover par rapport au déclencheur.',
      table: {
        type: { summary: 'start | center | end' },
        defaultValue: { summary: 'start' },
      },
    },
    trigger: { control: false, table: { disable: true } },
    default: { control: false, table: { disable: true } },
    class: { control: false, table: { disable: true } },
    style: { control: false, table: { disable: true } },
    key: { control: false, table: { disable: true } },
    ref: { control: false, table: { disable: true } },
    ref_for: { control: false, table: { disable: true } },
    ref_key: { control: false, table: { disable: true } },
  },
  args: {
    side: 'bottom',
    align: 'start',
  },
  render: (args: CspPopoverProps) => ({
    components: { CspPopover, CspButton },
    setup() {
      const { controlledOpen, handleUpdateOpen, open } = useStoryOpenState(args)

      return { args, controlledOpen, handleUpdateOpen, open }
    },
    template: `
      <CspPopover v-bind="args" :open="controlledOpen" @update:open="handleUpdateOpen">
        <template #trigger>
          <CspButton
            :label="(open ? 'Fermer' : 'Ouvrir') + ' le popover'"
            variant="secondary"
            icon="ri:settings-3-line"
            :is-icon-left="true"
          />
        </template>

        <p class="text-sm">Contenu libre du popover.</p>
      </CspPopover>
    `,
  }),
}

export default meta
type Story = StoryObj<CspPopoverProps>

export const Default: Story = {
  name: 'Par défaut',
}

export const Sides: Story = {
  name: 'Côtés',
  render: (args: CspPopoverProps) => ({
    components: { CspPopover, CspButton },
    setup() {
      const sides = [
        { label: 'Haut', value: 'top' },
        { label: 'Droite', value: 'right' },
        { label: 'Bas', value: 'bottom' },
        { label: 'Gauche', value: 'left' },
      ] satisfies { label: string, value: NonNullable<CspPopoverProps['side']> }[]

      return { args, sides }
    },
    template: `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `,
  }),
}

export const Alignments: Story = {
  name: 'Alignements',
  render: (args: CspPopoverProps) => ({
    components: { CspPopover, CspButton },
    setup() {
      const alignments = [
        { label: 'Début', value: 'start' },
        { label: 'Centre', value: 'center' },
        { label: 'Fin', value: 'end' },
      ] satisfies { label: string, value: NonNullable<CspPopoverProps['align']> }[]

      return { args, alignments }
    },
    template: `
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `,
  }),
}
