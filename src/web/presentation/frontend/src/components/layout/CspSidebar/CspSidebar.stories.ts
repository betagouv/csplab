import type { Meta, StoryObj } from '@storybook/vue3'
import CspAppLayout from '../CspAppLayout/CspAppLayout.vue'
import CspSidebar from './CspSidebar.vue'
import CspSidebarGroup from './CspSidebarGroup.vue'
import CspSidebarItem from './CspSidebarItem.vue'
import CspSidebarLogo from './CspSidebarLogo.vue'
import CspSidebarUser from './CspSidebarUser.vue'

const meta: Meta<typeof CspSidebar> = {
  title: 'Compositions/Layout/CspSidebar',
  component: CspSidebar,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: `
Sidebar de navigation principale de l'ATS.

- **Logo** avec sous-titre, **groupes de sections** étiquetés
- **Bouton toggle** fixe en haut à droite
- **Item actif** mis en avant par un fond plein bleu France
- **Footer** avec identité utilisateur
        `,
      },
    },
  },
  argTypes: {
    defaultExpanded: {
      control: 'boolean',
      description: 'État initial de la sidebar (ouverte ou fermée)',
    },
  },
}

export default meta

type Story = StoryObj<typeof CspSidebar>

const sidebarTemplate = `
  <CspAppLayout>
    <template #sidebar>
      <CspSidebar :defaultExpanded="defaultExpanded">
        <template #logo>
          <CspSidebarLogo />
        </template>

        <CspSidebarGroup label="Pilotage">
          <CspSidebarItem icon="ri:dashboard-line" label="Tableau de bord" />
          <CspSidebarItem icon="ri:briefcase-line" label="Mes offres" :isActive="true" />
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
      <h1 style="margin: 0 0 0.5rem; font-size: 1.5rem; font-weight: 600; color: var(--text-title-grey);">
        Mes offres
      </h1>
      <p style="color: var(--text-mention-grey); margin: 0;">
        Utilisez le bouton en haut de la sidebar pour l'ouvrir ou la réduire.
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
  CspSidebarUser,
}

export const Default: Story = {
  args: {
    defaultExpanded: true,
  },
  render: args => ({
    components,
    setup: () => ({ defaultExpanded: args.defaultExpanded }),
    template: sidebarTemplate,
  }),
}

export const Collapsed: Story = {
  args: {
    defaultExpanded: false,
  },
  render: args => ({
    components,
    setup: () => ({ defaultExpanded: args.defaultExpanded }),
    template: sidebarTemplate,
  }),
}
