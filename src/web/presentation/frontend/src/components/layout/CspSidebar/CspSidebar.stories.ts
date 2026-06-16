import type { Meta, StoryObj } from '@storybook/vue3-vite'
import CspAppLayout from '../CspAppLayout/CspAppLayout.vue'
import CspSidebar from './CspSidebar.vue'
import CspSidebarGroup from './CspSidebarGroup.vue'
import CspSidebarItem from './CspSidebarItem.vue'
import CspSidebarLogo from './CspSidebarLogo.vue'
import CspSidebarProvider from './CspSidebarProvider.vue'
import CspSidebarTrigger from './CspSidebarTrigger.vue'
import CspSidebarUser from './CspSidebarUser.vue'

const meta: Meta<typeof CspSidebarProvider> = {
  title: 'Compositions/Layout/CspSidebar',
  component: CspSidebarProvider,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: `
Sidebar de navigation adaptée au DSFR.

## Composants

- \`CspSidebarProvider\` : contexte partagé (état, mobile, raccourcis)
- \`CspSidebar\` : panneau de navigation
- \`CspSidebarTrigger\` : bouton hamburger mobile (dans le header)
- \`CspSidebarGroup\`, \`CspSidebarItem\`, \`CspSidebarLogo\`, \`CspSidebarUser\`

## Usage

\`\`\`vue
<CspSidebarProvider default-expanded>
  <CspAppLayout>
    <template #sidebar>
      <CspSidebar>...</CspSidebar>
    </template>
    <template #header>
      <CspSidebarTrigger />
    </template>
    <!-- contenu -->
  </CspAppLayout>
</CspSidebarProvider>
\`\`\`
        `,
      },
    },
  },
  argTypes: {
    defaultExpanded: {
      control: 'boolean',
      description: 'État initial de la sidebar (ouverte ou fermée)',
    },
    persistState: {
      control: 'boolean',
      description: 'Persister l\'état en cookie',
    },
  },
}

export default meta

type Story = StoryObj<typeof CspSidebarProvider>

const sidebarTemplate = `
  <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
    <CspAppLayout>
      <template #sidebar>
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup label="Pilotage">
            <CspSidebarItem icon="ri:dashboard-line" label="Tableau de bord" />
            <CspSidebarItem icon="ri:briefcase-line" label="Mes offres" :is-active="true" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Candidatures">
            <CspSidebarItem icon="ri:group-line" label="Toutes les candidatures" />
            <CspSidebarItem icon="ri:layout-column-line" label="Pipeline" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Entretiens">
            <CspSidebarItem icon="ri:calendar-line" label="Mes entretiens" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Paramètres">
            <CspSidebarItem icon="ri:settings-3-line" label="Paramètres" />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser name="Marie Dupont" role="RH" />
          </template>
        </CspSidebar>
      </template>

      <template #header>
        <CspSidebarTrigger />
      </template>

      <div style="padding: 2rem; max-width: 800px;">
        <h1 style="margin: 0 0 0.5rem; font-size: 1.5rem; font-weight: 600; color: var(--text-title-grey);">
          Mes offres
        </h1>
        <p style="color: var(--text-mention-grey); margin: 0 0 1rem;">
          Utilisez <kbd style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace; font-size: 0.75rem;">Ctrl+B</kbd> pour toggle la sidebar.
        </p>
        <p style="color: var(--text-mention-grey); margin: 0;">
          En mode collapsed, survolez les icônes pour voir les tooltips.
        </p>
      </div>
    </CspAppLayout>
  </CspSidebarProvider>
`

const components = {
  CspAppLayout,
  CspSidebar,
  CspSidebarGroup,
  CspSidebarItem,
  CspSidebarLogo,
  CspSidebarProvider,
  CspSidebarTrigger,
  CspSidebarUser,
}

export const Default: Story = {
  args: {
    defaultExpanded: true,
    persistState: false,
  },
  render: args => ({
    components,
    setup: () => ({ defaultExpanded: args.defaultExpanded, persistState: args.persistState }),
    template: sidebarTemplate,
  }),
}

export const Collapsed: Story = {
  args: {
    defaultExpanded: false,
    persistState: false,
  },
  render: args => ({
    components,
    setup: () => ({ defaultExpanded: args.defaultExpanded, persistState: args.persistState }),
    template: sidebarTemplate,
  }),
}

export const Mobile: Story = {
  args: {
    defaultExpanded: true,
    persistState: false,
  },
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
  render: args => ({
    components,
    setup: () => ({ defaultExpanded: args.defaultExpanded, persistState: args.persistState }),
    template: sidebarTemplate,
  }),
}
