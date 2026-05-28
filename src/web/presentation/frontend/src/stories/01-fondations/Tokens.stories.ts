import type { Meta, StoryObj } from '@storybook/vue3'

const meta = {
  title: '01 - Fondations/Tokens',
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

const COLOR_GROUPS: Array<{ group: string, tokens: string[] }> = [
  {
    group: 'Texte',
    tokens: [
      '--text-default-grey',
      '--text-title-grey',
      '--text-title-blue-france',
      '--text-action-high-blue-france',
      '--text-action-high-grey',
      '--text-mention-grey',
      '--text-disabled-grey',
      '--text-inverted-grey',
      '--text-default-info',
      '--text-default-success',
      '--text-default-warning',
      '--text-default-error',
    ],
  },
  {
    group: 'Fonds',
    tokens: [
      '--background-default-grey',
      '--background-alt-grey',
      '--background-alt-blue-france',
      '--background-contrast-grey',
      '--background-elevated-grey',
      '--background-contrast-info',
      '--background-contrast-success',
      '--background-contrast-warning',
      '--background-contrast-error',
      '--background-action-high-blue-france',
      '--background-action-high-blue-france-hover',
      '--background-action-high-blue-france-active',
      '--background-action-high-red-marianne',
      '--background-action-high-red-marianne-hover',
      '--background-action-high-red-marianne-active',
      '--background-default-grey-hover',
      '--background-default-grey-active',
      '--background-disabled-grey',
    ],
  },
  {
    group: 'Bordures',
    tokens: [
      '--border-default-grey',
      '--border-default-blue-france',
      '--border-action-high-blue-france',
      '--border-plain-info',
      '--border-plain-success',
      '--border-plain-warning',
      '--border-plain-error',
      '--border-disabled-grey',
      '--csplab-focus-ring-color',
    ],
  },
]

const SPACING_TOKENS = [
  '--csplab-space-1',
  '--csplab-space-2',
  '--csplab-space-3',
  '--csplab-space-4',
  '--csplab-space-5',
  '--csplab-space-6',
  '--csplab-space-8',
  '--csplab-space-10',
  '--csplab-space-12',
  '--csplab-space-16',
]

const FONT_SIZE_TOKENS = [
  { token: '--csplab-font-size-xs', label: 'xs — caption' },
  { token: '--csplab-font-size-sm', label: 'sm — meta / chip' },
  { token: '--csplab-font-size-base', label: 'base — body' },
  { token: '--csplab-font-size-md', label: 'md — body fort' },
  { token: '--csplab-font-size-lg', label: 'lg — sous-titre' },
  { token: '--csplab-font-size-xl', label: 'xl — titre section' },
  { token: '--csplab-font-size-2xl', label: '2xl — titre page' },
]

const FONT_WEIGHT_TOKENS = [
  { token: '--csplab-font-weight-regular', label: 'regular | 400' },
  { token: '--csplab-font-weight-medium', label: 'medium | 500' },
  { token: '--csplab-font-weight-bold', label: 'bold | 700' },
]

const LINE_HEIGHT_TOKENS = [
  { token: '--csplab-line-height-tight', label: 'tight | 1.25' },
  { token: '--csplab-line-height-base', label: 'base | 1.5' },
  { token: '--csplab-line-height-relaxed', label: 'relaxed | 1.625' },
]

const SHADOW_TOKENS = ['--csplab-shadow-sm', '--csplab-shadow-md', '--csplab-shadow-lg']

export const Couleurs: Story = {
  render: () => ({
    setup: () => ({ groups: COLOR_GROUPS }),
    template: `
      <div style="padding: var(--csplab-space-6); display: flex; flex-direction: column; gap: var(--csplab-space-8);">
        <section v-for="g in groups" :key="g.group">
          <h3 style="margin: 0 0 var(--csplab-space-3); font-size: var(--csplab-font-size-lg); color: var(--text-title-grey);">{{ g.group }}</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--csplab-space-3);">
            <div v-for="t in g.tokens" :key="t" style="border: 1px solid var(--border-default-grey); border-radius: var(--csplab-radius-md); overflow: hidden;">
              <div :style="{ background: 'var(' + t + ')', height: '56px' }"></div>
              <div style="padding: var(--csplab-space-2); font-family: ui-monospace, monospace; font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey); background: var(--background-default-grey);">{{ t }}</div>
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
      <div style="padding: var(--csplab-space-6); display: flex; flex-direction: column; gap: var(--csplab-space-3);">
        <div v-for="t in tokens" :key="t" style="display: flex; align-items: center; gap: var(--csplab-space-4);">
          <code style="width: 220px; font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
          <div :style="{ width: 'var(' + t + ')', height: '20px', background: 'var(--background-action-high-blue-france)', borderRadius: '2px' }"></div>
        </div>
      </div>
    `,
  }),
}

export const Typographie: Story = {
  render: () => ({
    setup: () => ({ fontSizes: FONT_SIZE_TOKENS, fontWeights: FONT_WEIGHT_TOKENS, lineHeights: LINE_HEIGHT_TOKENS }),
    template: `
      <div style="padding: var(--csplab-space-6); display: flex; flex-direction: column; gap: var(--csplab-space-8);">
        <section>
          <h3 style="margin: 0 0 var(--csplab-space-3); font-size: var(--csplab-font-size-lg); color: var(--text-title-grey);">Tailles</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csplab-space-4);">
            <div v-for="t in fontSizes" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csplab-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csplab-space-2);">
              <span :style="{ fontSize: 'var(' + t.token + ')', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csplab-space-3); font-size: var(--csplab-font-size-lg); color: var(--text-title-grey);">Graisses</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csplab-space-4);">
            <div v-for="t in fontWeights" :key="t.token" style="display: flex; align-items: baseline; gap: var(--csplab-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csplab-space-2);">
              <span :style="{ fontWeight: 'var(' + t.token + ')', fontSize: 'var(--csplab-font-size-md)', color: 'var(--text-title-grey)', minWidth: '280px' }">{{ t.label }}</span>
              <code style="font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
            </div>
          </div>
        </section>
        <section>
          <h3 style="margin: 0 0 var(--csplab-space-3); font-size: var(--csplab-font-size-lg); color: var(--text-title-grey);">Hauteurs de ligne</h3>
          <div style="display: flex; flex-direction: column; gap: var(--csplab-space-4);">
            <div v-for="t in lineHeights" :key="t.token" style="display: flex; align-items: flex-start; gap: var(--csplab-space-4); border-bottom: 1px solid var(--border-default-grey); padding-bottom: var(--csplab-space-2);">
              <p :style="{ lineHeight: 'var(' + t.token + ')', fontSize: 'var(--csplab-font-size-sm)', color: 'var(--text-title-grey)', minWidth: '280px', margin: 0 }">{{ t.label }}<br>Texte exemple sur deux lignes<br>pour visualiser l'interligne</p>
              <code style="font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey);">{{ t.token }}</code>
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
      <div style="padding: var(--csplab-space-8); display: flex; gap: var(--csplab-space-8); background: var(--background-alt-grey);">
        <div v-for="t in tokens" :key="t" style="text-align: center;">
          <div :style="{ width: '160px', height: '100px', background: 'var(--background-default-grey)', borderRadius: 'var(--csplab-radius-md)', boxShadow: 'var(' + t + ')', marginBottom: 'var(--csplab-space-3)' }"></div>
          <code style="font-size: var(--csplab-font-size-xs); color: var(--text-mention-grey);">{{ t }}</code>
        </div>
      </div>
    `,
  }),
}
