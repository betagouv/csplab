import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'

type CspTooltipProps = ComponentPropsAndSlots<typeof CspTooltip>

const meta = {
  title: 'Éléments/Génériques/CspTooltip',
  component: CspTooltip,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['content', 'side', 'align', 'sideOffset', 'delayDuration', 'disabled'],
    },
    docs: {
      description: {
        component: 'Infobulle contextuelle affichée au survol ou au focus. Enveloppe un élément déclencheur via le slot par défaut.',
      },
    },
  },
  argTypes: {
    content: {
      control: { type: 'text' },
      description: 'Texte affiché dans l\'infobulle.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    side: {
      control: { type: 'radio' },
      options: ['top', 'right', 'bottom', 'left'] satisfies NonNullable<CspTooltipProps['side']>[],
      description: 'Position de l\'infobulle par rapport au déclencheur.',
      table: {
        type: {
          summary: 'top | right | bottom | left',
        },
        defaultValue: {
          summary: 'right',
        },
      },
    },
    align: {
      control: { type: 'radio' },
      options: ['start', 'center', 'end'] satisfies NonNullable<CspTooltipProps['align']>[],
      description: 'Alignement de l\'infobulle le long de l\'axe perpendiculaire.',
      table: {
        type: {
          summary: 'start | center | end',
        },
        defaultValue: {
          summary: 'center',
        },
      },
    },
    sideOffset: {
      control: { type: 'number' },
      description: 'Distance entre l\'infobulle et le déclencheur, en pixels.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '8',
        },
      },
    },
    delayDuration: {
      control: { type: 'number' },
      description: 'Délai avant l\'affichage, en millisecondes.',
      table: {
        type: {
          summary: 'number',
        },
        defaultValue: {
          summary: '200',
        },
      },
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Désactive l\'infobulle et rend uniquement le contenu du slot.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
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
    content: 'Texte de l\'infobulle',
    side: 'top',
    align: 'center',
    sideOffset: 8,
    delayDuration: 200,
    disabled: false,
  },
  render: (args: CspTooltipProps) => ({
    components: { CspTooltip, CspButton },
    setup() {
      return { args }
    },
    template: `
      <div class="flex justify-center p-16">
        <CspTooltip v-bind="args">
          <CspButton label="Survolez-moi" />
        </CspTooltip>
      </div>
    `,
  }),
}

export default meta
type Story = StoryObj<CspTooltipProps>

const SIDES = ['top', 'right', 'bottom', 'left'] as const
const ALIGNS = ['start', 'center', 'end'] as const

export const Default: Story = {}

export const Positions: Story = {
  render: args => ({
    components: { CspTooltip, CspButton },
    setup() {
      return { sides: SIDES, args }
    },
    template: `
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="side in sides"
          :key="side"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            :side="side"
            :content="\`Position \${side}\`"
          >
            <CspButton
              :label="side"
              variant="secondary"
            />
          </CspTooltip>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const Alignments: Story = {
  render: args => ({
    components: { CspTooltip, CspButton },
    setup() {
      return { aligns: ALIGNS, args }
    },
    template: `
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="align in aligns"
          :key="align"
          class="flex flex-col items-center gap-2"
        >
          <CspTooltip
            v-bind="args"
            side="bottom"
            :align="align"
            :content="\`Alignement \${align}\`"
          >
            <CspButton
              :label="align"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}

export const LongContent: Story = {
  args: {
    content: 'Infobulle avec un contenu plus long pour vérifier le retour à la ligne et la largeur maximale.',
  },
}

export const Disabled: Story = {
  args: {
    content: 'Ce texte ne s\'affichera pas',
    disabled: true,
  },
}

export const Delays: Story = {
  render: args => ({
    components: { CspTooltip, CspButton },
    setup() {
      return {
        delays: [0, 200, 800] as const,
        args,
      }
    },
    template: `
      <div class="flex flex-wrap gap-12 justify-center p-16">
        <div
          v-for="delay in delays"
          :key="delay"
          class="flex flex-col items-center gap-2"
        >
          <p class="text-sm">{{ delay }} ms</p>
          <CspTooltip
            v-bind="args"
            :delay-duration="delay"
            :content="\`Délai de \${delay} ms\`"
          >
            <CspButton
              :label="\`\${delay} ms\`"
              variant="tertiary"
            />
          </CspTooltip>
        </div>
      </div>
    `,
  }),
  parameters: {
    controls: { disable: true },
  },
}
