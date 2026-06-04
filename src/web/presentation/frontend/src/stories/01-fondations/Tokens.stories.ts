import type { Meta, StoryObj } from '@storybook/vue3'
import { dsfrTokens } from './colors'

const meta = {
  title: 'Fondations/Tokens',
  parameters: {
    docs: {
      description: {
        component:
          'Catalogue visuel des tokens DSFR + extensions CSPLab.\n\n',
      },
    },
  },
} satisfies Meta

export default meta
type Story = StoryObj<typeof meta>

const SPACING_TOKENS = [
  '--csp-space-1',
  '--csp-space-2',
  '--csp-space-3',
  '--csp-space-4',
  '--csp-space-5',
  '--csp-space-6',
  '--csp-space-8',
  '--csp-space-10',
  '--csp-space-12',
  '--csp-space-16',
]

const FONT_SIZE_TOKENS = [
  { token: '--csp-font-size-xs', label: 'xs - caption' },
  { token: '--csp-font-size-sm', label: 'sm - meta / chip' },
  { token: '--csp-font-size-base', label: 'base - body' },
  { token: '--csp-font-size-md', label: 'md - body fort' },
  { token: '--csp-font-size-lg', label: 'lg - sous-titre' },
  { token: '--csp-font-size-xl', label: 'xl - titre section' },
  { token: '--csp-font-size-2xl', label: '2xl - titre page' },
]

const FONT_WEIGHT_TOKENS = [
  { token: '--csp-font-weight-regular', label: 'regular | 400' },
  { token: '--csp-font-weight-medium', label: 'medium | 500' },
  { token: '--csp-font-weight-bold', label: 'bold | 700' },
]

const LINE_HEIGHT_TOKENS = [
  { token: '--csp-line-height-tight', label: 'tight | 1.25' },
  { token: '--csp-line-height-base', label: 'base | 1.5' },
  { token: '--csp-line-height-relaxed', label: 'relaxed | 1.625' },
]

const SHADOW_TOKENS = ['--csp-shadow-sm', '--csp-shadow-md', '--csp-shadow-lg']

export const Couleurs: Story = {
  render: () => ({
    setup: () => ({ dsfrTokens }),
    template: `
      <div class="flex flex-col gap-12">
        <section
          v-for="g in dsfrTokens"
          :key="g.name"
        >
          <h3 class="text-2xl font-bold mb-2">
            {{ g.name }}
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-12 gap-y-8 border p-6">
            <div
              v-for="t in g.tokens"
              :key="t"
            >
              <template v-if="g.type === 'text'">
                <p
                  class="text-2xl font-medium"
                  :class="[
                    { ['bg-[#333]']: t.match('inverted') },
                  ]"
                  :style="{ color: 'var(--' + t + ')' }">
                  Lorem ipsum
                </p>
                <p class="text-[var(--text-mention-grey)]">
                  {{ t }}
                </p>
              </template>
              <template v-else-if="g.type === 'border'">
                <div
                  class="border-2 p-2"
                  :style="{ borderColor: 'var(--' + t + ')' }"
                  >
                  <p class="text-[var(--text-mention-grey)]">
                    {{ t }}
                  </p>
                </div>
              </template>
              <template v-else>
                <div class="flex flex-col gap-2">
                  <div class="flex flex-row gap-2">
                    <div
                      v-for="tok in new Array(g.interactive ? 3 : 1)
                        .fill(null)
                        .map((_, i) => {
                          return t + ['', '-hover', '-active'][i]
                        })"
                      :key="tok"
                      class="flex-1 h-12 border border-black"
                      :style="{ background: 'var(--' + tok + ')' }"
                    />
                  </div>
                  <div class="text-[var(--text-mention-grey)]">
                    <p>
                      {{ t }}
                    </p>
                    <template
                      v-if="g.interactive"
                    >
                      <p>
                        {{ t }}-hover
                      </p>
                      <p>
                        {{ t }}-active
                      </p>
                    </template>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </section>
      </div>
    `,
  }),
}

export const Espacements: Story = {
  render: () => ({
    setup: () => ({ tokens: SPACING_TOKENS }),
    template: `
      <div class="flex flex-col gap-12">
        <section>
          <h3 class="text-2xl font-bold mb-2">Espacements</h3>
          <div class="flex flex-col gap-3 border p-6">
            <div
              v-for="t in tokens"
              :key="t"
              class="flex items-center gap-4"
            >
              <code class="w-52 text-xs text-[var(--text-mention-grey)]">{{ t }}</code>
              <div
                class="h-5 bg-[var(--background-action-high-blue-france)] rounded-sm"
                :style="{ width: 'var(' + t + ')' }"
              />
            </div>
          </div>
        </section>
      </div>
    `,
  }),
}

export const Typographie: Story = {
  render: () => ({
    setup: () => ({ fontSizes: FONT_SIZE_TOKENS, fontWeights: FONT_WEIGHT_TOKENS, lineHeights: LINE_HEIGHT_TOKENS }),
    template: `
      <div class="flex flex-col gap-12">
        <section>
          <h3 class="text-2xl font-bold mb-4">Tailles</h3>
          <div class="flex flex-col gap-4 border p-6">
            <div
              v-for="t in fontSizes"
              :key="t.token"
              class="flex items-baseline gap-4 border-b border-[var(--border-default-grey)] pb-2"
            >
              <span
                class="min-w-[280px] text-[var(--text-title-grey)]"
                :style="{ fontSize: 'var(' + t.token + ')' }"
              >
                {{ t.label }}
              </span>
              <code class="text-xs text-[var(--text-mention-grey)]">{{ t.token }}</code>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-2xl font-bold mb-4">Graisses</h3>
          <div class="flex flex-col gap-4 border p-6">
            <div
              v-for="t in fontWeights"
              :key="t.token"
              class="flex items-baseline gap-4 border-b border-[var(--border-default-grey)] pb-2"
            >
              <span
                class="min-w-[280px] text-[var(--text-title-grey)] text-md"
                :style="{ fontWeight: 'var(' + t.token + ')' }"
              >
                {{ t.label }}
              </span>
              <code class="text-xs text-[var(--text-mention-grey)]">{{ t.token }}</code>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-2xl font-bold mb-4">Hauteurs de ligne</h3>
          <div class="flex flex-col gap-4 border p-6">
            <div
              v-for="t in lineHeights"
              :key="t.token"
              class="flex items-start gap-4 border-b border-[var(--border-default-grey)] pb-2"
            >
              <p
                class="min-w-[280px] text-[var(--text-title-grey)] text-sm m-0"
                :style="{ lineHeight: 'var(' + t.token + ')' }"
              >
                {{ t.label }}<br>Texte exemple sur deux lignes<br>pour visualiser l'interligne
              </p>
              <code class="text-xs text-[var(--text-mention-grey)]">{{ t.token }}</code>
            </div>
          </div>
        </section>
      </div>
    `,
  }),
}

export const Ombres: Story = {
  render: () => ({
    setup: () => ({ tokens: SHADOW_TOKENS }),
    template: `
      <div class="flex flex-col gap-12">
        <section>
          <h3 class="text-2xl font-bold mb-4">Ombres</h3>
          <div class="flex gap-8 border p-8 bg-[var(--background-alt-grey)]">
            <div
              v-for="t in tokens"
              :key="t"
              class="text-center"
            >
              <div
                class="w-40 h-[100px] bg-[var(--background-default-grey)] rounded-[var(--csp-radius-md)] mb-3"
                :style="{ boxShadow: 'var(' + t + ')' }"
              />
              <code class="text-xs text-[var(--text-mention-grey)]">{{ t }}</code>
            </div>
          </div>
        </section>
      </div>
    `,
  }),
}
