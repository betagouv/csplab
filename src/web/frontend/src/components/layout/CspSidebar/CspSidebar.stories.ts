import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { CspSidebarSwitcherGroup } from './CspSidebarSwitcher.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import CspSidebar from './CspSidebar.vue'
import CspSidebarGroup from './CspSidebarGroup.vue'
import CspSidebarItem from './CspSidebarItem.vue'
import CspSidebarLogo from './CspSidebarLogo.vue'
import CspSidebarProvider from './CspSidebarProvider.vue'
import CspSidebarSwitcher from './CspSidebarSwitcher.vue'
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
- \`CspSidebarSwitcher\` : sélecteur d'espace, avec recherche facultative ; un bloc fixe quand la liste a un seul choix et aucune recherche

## Slots

- \`logo\` : en-tête, à la hauteur du fil d'Ariane de la page
- \`context\` : sous l'en-tête, à la hauteur du titre de la page (sélecteur d'espace ou d'organisme)
- défaut : entrées de navigation, groupées par \`CspSidebarGroup\`
- \`footer\` : bas de panneau (utilisateur)

## Usage

\`\`\`vue
<CspAppShell :navigation="navigation">
  <!-- contenu de page -->
</CspAppShell>
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
    <div style="display: flex; min-height: 100vh;">
      <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
        <CspSidebar>
          <template #logo>
            <CspSidebarLogo />
          </template>

          <CspSidebarGroup>
            <CspSidebarItem icon="ri:dashboard-line" label="Première entrée" :to="{ path: '/premiere' }" />
            <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
          </CspSidebarGroup>

          <CspSidebarGroup>
            <CspSidebarItem icon="ri:group-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
            <CspSidebarItem icon="ri:layout-column-line" label="Quatrième entrée" :to="{ path: '/quatrieme' }" />
          </CspSidebarGroup>

          <CspSidebarGroup>
            <CspSidebarItem icon="ri:settings-3-line" label="Cinquième entrée" :to="{ path: '/cinquieme' }" />
          </CspSidebarGroup>

          <template #footer>
            <CspSidebarUser name="Prénom Nom" role="Rôle" />
          </template>
        </CspSidebar>
      </aside>

      <div style="flex: 1; min-width: 0;">
        <header style="display: flex; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-default-grey);">
          <CspSidebarTrigger />
        </header>

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
      </div>
    </div>
  </CspSidebarProvider>
`

const components = {
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
        <div style="display: flex; min-height: 100vh;">
          <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
            <CspSidebar>
              <template #logo>
                <CspSidebarLogo />
              </template>

              <CspSidebarGroup>
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
          </aside>

          <div style="flex: 1; min-width: 0;">
            <header style="display: flex; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-default-grey);">
              <CspSidebarTrigger />
            </header>

            <div style="padding: 2rem;">
              <p style="color: var(--text-mention-grey); margin: 0;">
                Cliquez une entrée pour naviguer. Route active :
                <code style="padding: 0.125rem 0.375rem; border-radius: 0.25rem; background: var(--background-contrast-grey); font-family: monospace;">{{ route.path }}</code>
              </p>
            </div>
          </div>
        </div>
      </CspSidebarProvider>
    `,
  }),
}

const ATELIER = { value: 'atelier', label: 'Atelier des Hautes-Alpes' }
const COOPERATIVE = { value: 'cooperative', label: 'Coopérative des producteurs de la vallée de la Haute-Durance' }
const ASSOCIATION = { value: 'association', label: 'Association des usagers du réseau de transport' }
const ESPACES = [ATELIER, COOPERATIVE, ASSOCIATION]

function contextStory(switcher: {
  title: string
  selected: string
  groupsFor: (search: string) => CspSidebarSwitcherGroup[]
  filterLabel?: string
}, description: string): Story {
  return {
    args: {
      defaultExpanded: true,
      persistState: false,
    },
    parameters: {
      docs: {
        description: { story: description },
      },
    },
    render: args => ({
      components: { ...components, CspAvatar, CspSidebarSwitcher, CspPageHeader },
      setup() {
        const search = ref('')
        const groups = computed(() => switcher.groupsFor(search.value))
        const breadcrumb = [{ label: 'Accueil', to: '/' }, { label: 'Page' }]
        const ariaLabel = `${switcher.title}. Changer d'espace`
        return {
          defaultExpanded: args.defaultExpanded,
          persistState: args.persistState,
          switcher,
          ariaLabel,
          search,
          groups,
          breadcrumb,
        }
      },
      template: `
        <CspSidebarProvider :default-expanded="defaultExpanded" :persist-state="persistState">
          <div style="display: flex; min-height: 100vh;">
            <aside style="flex-shrink: 0; border-right: 1px solid var(--border-default-grey);">
              <CspSidebar>
                <template #logo>
                  <CspSidebarLogo />
                </template>

                <template #context>
                  <CspSidebarSwitcher
                    v-model:search="search"
                    :title="switcher.title"
                    :groups="groups"
                    :selected="switcher.selected"
                    :filter-label="switcher.filterLabel"
                    :aria-label="ariaLabel"
                  >
                    <template #leading>
                      <CspAvatar icon="ri:government-fill" />
                    </template>
                  </CspSidebarSwitcher>
                </template>

                <CspSidebarGroup>
                  <CspSidebarItem icon="ri:briefcase-line" label="Entrée active" :to="{ path: '/active' }" :is-active="true" />
                  <CspSidebarItem icon="ri:group-line" label="Deuxième entrée" :to="{ path: '/deuxieme' }" />
                </CspSidebarGroup>

                <CspSidebarGroup>
                  <CspSidebarItem icon="ri:settings-3-line" label="Troisième entrée" :to="{ path: '/troisieme' }" />
                </CspSidebarGroup>

                <template #footer>
                  <CspSidebarUser name="Prénom Nom" role="Rôle" />
                </template>
              </CspSidebar>
            </aside>

            <div style="flex: 1; min-width: 0;">
              <CspPageHeader title="Titre de la page" :breadcrumb="breadcrumb">
                <template #subtitle>
                  <p style="margin: 0; color: var(--text-mention-grey);">Sous-titre de la page</p>
                </template>
              </CspPageHeader>
            </div>
          </div>
        </CspSidebarProvider>
      `,
    }),
  }
}

export const WithContext: Story = {
  name: 'Avec sélecteur de contexte',
  ...contextStory({
    title: COOPERATIVE.label,
    selected: COOPERATIVE.value,
    groupsFor: () => [{ label: 'Changer d\'espace', options: ESPACES }],
  }, 'Le slot `context` reçoit un sélecteur d\'espace ou d\'organisme, à la hauteur du titre de la page ; la navigation commence sous la ligne de l\'en-tête. La zone est réservée même sans contenu.'),
}

export const WithSearchableContext: Story = {
  name: 'Avec sélecteur de contexte et recherche',
  ...contextStory({
    title: 'Vue d\'ensemble',
    selected: 'ensemble',
    filterLabel: 'Rechercher un espace',
    groupsFor: (search) => {
      const term = search.trim().toLowerCase()
      if (term) {
        return [{ options: ESPACES.filter(espace => espace.label.toLowerCase().includes(term)) }]
      }
      return [
        { options: [{ value: 'ensemble', label: 'Vue d\'ensemble' }] },
        { label: 'Récents', options: [ATELIER, COOPERATIVE] },
      ]
    },
  }, 'Avec `filterLabel`, le menu commence par un champ de recherche ; le parent filtre les groupes à partir de `v-model:search`. Le sélecteur vide la recherche à la fermeture.'),
}

export const WithSingleContext: Story = {
  name: 'Avec un seul contexte',
  ...contextStory({
    title: ATELIER.label,
    selected: ATELIER.value,
    groupsFor: () => [{ options: [ATELIER] }],
  }, 'Avec un seul choix et sans recherche, le sélecteur devient un bloc fixe, sans menu.'),
}
