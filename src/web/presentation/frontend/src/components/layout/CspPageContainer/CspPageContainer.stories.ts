import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'

type CspPageContainerProps = ComponentPropsAndSlots<typeof CspPageContainer>

const meta = {
  title: 'Compositions/Génériques/CspPageContainer',
  component: CspPageContainer,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
    controls: {
      include: ['width', 'fill'],
    },
    docs: {
      description: {
        component: 'Conteneur de page, sert de référence aux container queries (`@container page`). Voir DDR-005.',
      },
    },
  },
  argTypes: {
    width: {
      control: { type: 'select' },
      options: ['reading', 'wide', 'full'],
      description: 'Largeur du contenu.',
      table: {
        type: {
          summary: '\'reading\' | \'wide\' | \'full\'',
        },
        defaultValue: {
          summary: '\'wide\'',
        },
      },
    },
  },
}

export default meta
type Story = StoryObj<CspPageContainerProps>

export const Widths: Story = {
  name: 'Largeurs',
  args: {
    width: 'reading',
  },
  render: (args: CspPageContainerProps) => ({
    components: { CspPageContainer },
    setup() {
      const widths = ['reading', 'wide', 'full'] as const
      return { args, widths }
    },
    template: `
      <div class="flex flex-col">
        <CspPageContainer v-for="width in widths" :key="width" v-bind="args" :width="width">
          <div class="border border-dashed border-(--border-default-grey) p-4">
            Contenu du conteneur (largeur : {{ width }})
          </div>
        </CspPageContainer>
      </div>
    `,
  }),
}
