import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3'
import BaseButton from '@/components/base/BaseButton/BaseButton.vue'

type ButtonProps = ComponentPropsAndSlots<typeof BaseButton>

const meta = {
  title: '02 - Elements/Generic/BaseButton',
  component: BaseButton,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['variant', 'size', 'isIconLeft', 'label', 'icon', 'as', 'asChild'],
    },
    docs: {
      description: {
        component: 'Generic button. Either have a `label` or an `icon` or both.',
      },
    },
  },
  argTypes: {
    variant: {
      control: { type: 'radio' },
      options: ['primary', 'secondary', 'tertiary', 'tertiary-no-outline'] satisfies ButtonProps['variant'][],
      description: 'Visual style.',
      table: {
        type: {
          summary: 'primary | secondary | tertiary | tertiary-no-outline',
        },
        defaultValue: {
          summary: 'primary',
        },
      },
    },
    size: {
      control: { type: 'radio' },
      options: ['sm', 'md', 'lg'] satisfies ButtonProps['size'][],
      description: 'Button size.',
      table: {
        type: {
          summary: 'sm | md | lg',
        },
        defaultValue: {
          summary: 'md',
        },
      },
    },
    isIconLeft: {
      control: { type: 'boolean' },
      description: 'Show icon before label.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
      },
    },
    label: {
      control: { type: 'text' },
      description: 'Button text. Required if `icon` is missing.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    icon: {
      control: { type: 'text' },
      description: 'Iconify name. Required if `label` is missing.',
      table: {
        type: {
          summary: 'string',
        },
      },
    },
    as: {
      control: { type: 'text' },
      description: 'Rendered element or component.',
      table: {
        type: {
          summary: 'string | Component',
        },
        defaultValue: {
          summary: 'button',
        },
      },
    },
    asChild: {
      control: { type: 'boolean' },
      description: 'Render the child as the root element.',
      table: {
        type: {
          summary: 'boolean',
        },
        defaultValue: {
          summary: 'false',
        },
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
    variant: 'primary',
    size: 'md',
    isIconLeft: false,
    label: 'Button label',
    asChild: false,
  },
  render: (args: ButtonProps) => ({
    components: { BaseButton },
    setup() {
      return { args }
    },
    template: '<BaseButton v-bind="args" />',
  }),
}

export default meta
type Story = StoryObj<ButtonProps>

const VARIANTS = ['primary', 'secondary', 'tertiary', 'tertiary-no-outline'] as const
const SIZES = ['sm', 'md', 'lg'] as const

export const Default: Story = {
  args: {
    label: 'Button label',
  },
}

export const Variants: Story = {
  render: args => ({
    components: { BaseButton },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex flex-row gap-12">
        <div
          v-for="v in variants"
          :key="v"
        >
          <p class="mb-2">{{ v }}</p>
          <BaseButton
            v-bind="args"
            :variant="v"
            label="Label"
          />
        </div>
      </div>
    `,
  }),
}

export const Sizes: Story = {
  render: args => ({
    components: { BaseButton },
    setup() {
      return { sizes: SIZES, args }
    },
    template: `
      <div class="flex flex-row gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p class="mb-2">{{ s }}</p>
          <BaseButton
            v-bind="args"
            :size="s"
            label="Label"
          />
        </div>
      </div>
    `,
  }),
}

export const Icons: Story = {
  render: args => ({
    components: { BaseButton },
    setup() {
      const iconVariants = [
        {
          description: 'No icon',
          props: {
            label: 'Label',
          },
        },
        {
          description: 'Icon right',
          props: {
            label: 'Label',
            icon: 'ri:arrow-right-line',
          },
        },
        {
          description: 'Icon left',
          props: {
            label: 'Label',
            icon: 'ri:arrow-left-line',
            isIconLeft: true,
          },
        },
        {
          description: 'Icon only',
          props: {
            icon: 'ri:checkbox-circle-line',
            label: undefined,
          },
        },
      ] as const
      return { args, iconVariants, sizes: SIZES }
    },
    template: `
      <div class="flex flex-col gap-12">
        <div
          v-for="s in sizes"
          :key="s"
        >
          <p>{{ s }}</p>
          <div class="flex flex-row gap-12">
            <div
              v-for="v in iconVariants"
              :key="v.description"
            >
              <p class="mb-2">{{ v.description }}</p>
              <BaseButton
                v-bind="{ ...args, ...v.props }"
                :size="s"
              />
            </div>
          </div>
        </div>
      </div>
    `,
  }),
}

export const States: Story = {
  render: args => ({
    components: { BaseButton },
    setup() {
      return { variants: VARIANTS, args }
    },
    template: `
      <div class="flex flex-col gap-3">
        <div
          v-for="v in variants"
          :key="v"
          class="flex gap-3 items-center"
        >
          <p class="w-24">{{ v }}</p>
          <BaseButton
            :variant="v"
            v-bind="args"
            label="Default"
          />
          <BaseButton
            :variant="v"
            v-bind="args"
            :disabled="true"
            label="Disabled"
          />
        </div>
      </div>
    `,
  }),
}

export const AsLink: Story = {
  render: () => ({
    components: { BaseButton },
    template: `
      <BaseButton
        as="a"
        href="https://www.csplab.beta.gouv.fr"
        target="_blank"
        label="Visit CSPLab"
        icon="ri:external-link-line"
      />
    `,
  }),
}
