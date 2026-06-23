import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { useRoute } from 'vue-router'
import CspAppLayout from '../CspAppLayout/CspAppLayout.vue'
import CspSidebar from './CspSidebar.vue'
import CspSidebarGroup from './CspSidebarGroup.vue'
import CspSidebarItem from './CspSidebarItem.vue'
import CspSidebarLogo from './CspSidebarLogo.vue'
import CspSidebarProvider from './CspSidebarProvider.vue'
import CspSidebarTrigger from './CspSidebarTrigger.vue'
import CspSidebarUser from './CspSidebarUser.vue'

const meta: Meta<typeof CspSidebarProvider> = {
  title: 'Compositions/Génériques/CspSidebar',
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

          <CspSidebarGroup label="Groupe A">
            <CspSidebarItem icon="ri:dashboard-line" label="Première entrée" :to="{ path: '/premiere' }" />
            <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Groupe B">
            <CspSidebarItem icon="ri:group-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
            <CspSidebarItem icon="ri:layout-column-line" label="Quatrième entrée" :to="{ path: '/quatrieme' }" />
          </CspSidebarGroup>

          <CspSidebarGroup label="Groupe C">
            <CspSidebarItem icon="ri:settings-3-line" label="Cinquième entrée" :to="{ path: '/cinquieme' }" />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser name="Prénom Nom" role="Rôle" />
          </template>
        </CspSidebar>
      </template>

      <template #header>
        <CspSidebarTrigger />
      </template>

      <div style="padding: 2rem; max-width: 800px;">
        <h1 style="margin: 0 0 0.5rem; font-size: 1.5rem; font-weight: 600; color: var(--text-title-grey);">
          Contenu
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

export const WithRouterLinks: Story = {
  name: 'Avec liens de navigation',
  args: {
    defaultExpanded: true,
    persistState: false,
  },
  parameters: {
    docs: {
      description: {
        story: 'Navigation simulée : cliquer une entrée change la route (historique mémoire) et met à jour l\'état actif en direct. Permet de tester les états actif / inactif sans câbler `is-active` à la main.',
      },
    },
  },
  render: args => ({
    components,
    setup() {
      const route = useRoute()
      const items = [
        { icon: 'ri:dashboard-line', label: 'Première entrée', to: '/premiere' },
        { icon: 'ri:briefcase-line', label: 'Deuxième entrée', to: '/deuxieme' },
        { icon: 'ri:group-line', label: 'Troisième entrée', to: '/troisieme' },
        { icon: 'ri:settings-3-line', label: 'Quatrième entrée', to: '/quatrieme' },
      ]
      return {
        defaultExpanded: args.defaultExpanded,
        persistState: args.persistState,
        route,
        items,
      }
    },
    template: `
      <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
        <CspAppLayout>
          <template #sidebar>
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <CspSidebarGroup label="Navigation">
                <CspSidebarItem
                  v-for="item in items"
                  :key="item.to"
                  :icon="item.icon"
                  :label="item.label"
                  :to="item.to"
                  :is-active="route.path === item.to"
                />
              </CspSidebarGroup>
            </CspSidebar>
          </template>

          <template #header>
            <CspSidebarTrigger />
          </template>

          <div style="padding: 2rem;">
            <p style="color: var(--text-mention-grey); margin: 0;">
              Cliquez une entrée pour naviguer. Route active :
              <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
            </p>
          </div>
        </CspAppLayout>
      </CspSidebarProvider>
    `,
  }),
}
