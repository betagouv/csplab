import type { Meta, StoryObj } from '@storybook/vue3'
import CspAppLayout from '../CspAppLayout/CspAppLayout.vue'
import CspSidebar from './CspSidebar.vue'
import CspSidebarGroup from './CspSidebarGroup.vue'
import CspSidebarItem from './CspSidebarItem.vue'
import CspSidebarLogo from './CspSidebarLogo.vue'
import CspSidebarTrigger from './CspSidebarTrigger.vue'
import CspSidebarUser from './CspSidebarUser.vue'

const meta: Meta<typeof CspSidebar> = {
  title: 'Compositions/Layout/CspSidebar',
  component: CspSidebar,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: `
Sidebar de navigation inspirée de shadcn-vue, adaptée au DSFR.

## Fonctionnalités

- **Responsive** : drawer mobile avec overlay, sidebar fixe desktop
- **Raccourci clavier** : \`Ctrl+B\` pour toggle
- **Tooltips** : affichés en mode collapsed pour accessibilité
- **Persistance** : état sauvegardé en cookie
- **Accessible** : ARIA labels, focus management, navigation clavier

## Composants

- \`CspSidebar\` : conteneur principal (provider)
- \`CspSidebarGroup\` : groupe de liens avec label
- \`CspSidebarItem\` : lien de navigation
- \`CspSidebarLogo\` : logo et sous-titre
- \`CspSidebarUser\` : identité utilisateur en footer
- \`CspSidebarTrigger\` : bouton hamburger pour mobile

## Usage

\`\`\`vue
<CspSidebar default-expanded>
  <template #logo>
    <CspSidebarLogo />
  </template>

  <CspSidebarGroup label="Section">
    <CspSidebarItem icon="ri:home-line" label="Accueil" />
    <CspSidebarItem icon="ri:settings-line" label="Paramètres" is-active />
  </CspSidebarGroup>

  <template #footer>
    <CspSidebarUser name="Jean Dupont" role="Admin" />
  </template>
</CspSidebar>
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

type Story = StoryObj<typeof CspSidebar>

const sidebarTemplate = `
  <CspAppLayout>
    <template #sidebar>
      <CspSidebar :default-expanded="defaultExpanded" :persist-state="persistState">
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

    <div style="padding: 2rem; max-width: 800px;">
      <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <CspSidebarTrigger />
        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 600; color: var(--text-title-grey);">
          Mes offres
        </h1>
      </div>
      <p style="color: var(--text-mention-grey); margin: 0 0 1rem;">
        Utilisez <kbd style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace; font-size: 0.75rem;">Ctrl+B</kbd> pour toggle la sidebar.
      </p>
      <p style="color: var(--text-mention-grey); margin: 0;">
        En mode collapsed, survolez les icônes pour voir les tooltips.
      </p>
    </div>
  </CspAppLayout>
`

const components = {
  CspAppLayout,
  CspSidebar,
  CspSidebarGroup,
  CspSidebarItem,
  CspSidebarLogo,
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
