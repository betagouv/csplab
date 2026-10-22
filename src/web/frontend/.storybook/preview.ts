import type { Preview } from '@storybook/vue3'
import { PiniaColada } from '@pinia/colada'
import { setup } from '@storybook/vue3'
import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { sb } from 'storybook/test'
import { computed, provide } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { applyUnreadColor, DEFAULT_UNREAD_COLOR, DEFAULT_UNREAD_VARIANT, UNREAD_COLORS, UNREAD_VARIANT_KEY, UNREAD_VARIANTS } from '../src/app/prototypes/messages-non-lus/variants'
import { routes } from '../src/router/routes'
import { applyScenario, DEFAULT_SCENARIO, SCENARIOS } from '../src/styles/etiquettes/scenarios'
import '../src/app/icons'
import '../src/app/prototypes/messages-non-lus/couleurs.css'
import '../src/styles/index.css'
import './storybook.css'

// Demo data for the prototype screens: each module is replaced by the file of the same name in its __mocks__ folder.
sb.mock('../src/api/utilisateur.ts')
sb.mock('../src/features/candidatures/api.ts')
sb.mock('../src/features/messages/api.ts')
sb.mock('../src/features/recrutements/api.ts')
sb.mock('@pinia/colada-devtools')

const storybookRouter = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/:pathMatch(.*)*', component: { template: '<div />' } }],
})

// A story with parameters.appRoute renders the application routes in memory, with its stores.
setup(async (app, context) => {
  const appRoute: string | undefined = context?.parameters.appRoute
  if (!appRoute) {
    app.use(storybookRouter)
    return
  }
  const router = createRouter({ history: createMemoryHistory(), routes })
  await router.push(appRoute)
  app.use(createPinia())
  app.use(PiniaColada, { queryOptions: { staleTime: 5 * 60 * 1000, refetchOnWindowFocus: false } })
  app.use(router)
  app.use(createHead())
})

function applyTheme(theme: string) {
  localStorage.setItem('csp_color_mode', theme)
  document.documentElement.setAttribute('data-fr-theme', theme)
}

const NO_SCENARIO = 'repli'

const preview: Preview = {
  initialGlobals: {
    theme: 'light',
    etiquettes: DEFAULT_SCENARIO ?? NO_SCENARIO,
    nonLus: DEFAULT_UNREAD_VARIANT,
    nonLusCouleur: DEFAULT_UNREAD_COLOR,
  },
  globalTypes: {
    theme: {
      description: 'Thème DSFR',
      toolbar: {
        title: 'Thème',
        icon: 'contrast',
        items: [
          { value: 'light', title: 'Clair', icon: 'sun' },
          { value: 'dark', title: 'Sombre', icon: 'moon' },
        ],
        dynamicTitle: true,
      },
    },
    etiquettes: {
      description: 'Scénario de couleurs des étiquettes',
      toolbar: {
        title: 'Étiquettes',
        icon: 'paintbrush',
        items: [
          { value: NO_SCENARIO, title: 'Repli gris' },
          ...SCENARIOS.map(({ id, name }) => ({ value: id, title: name })),
        ],
        dynamicTitle: true,
      },
    },
    nonLus: {
      description: 'Signalement des messages non lus sur les cartes du kanban',
      toolbar: {
        title: 'Non lus',
        icon: 'email',
        items: UNREAD_VARIANTS.map(({ id, name }) => ({ value: id, title: name })),
        dynamicTitle: true,
      },
    },
    nonLusCouleur: {
      description: 'Couleur du signal des messages non lus',
      toolbar: {
        title: 'Couleur des non-lus',
        icon: 'circle',
        items: UNREAD_COLORS.map(({ id, name }) => ({ value: id, title: name })),
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (story, context) => {
      applyTheme(context.globals.theme ?? 'light')
      applyScenario(document.documentElement, context.globals.etiquettes)
      applyUnreadColor(document.documentElement, context.globals.nonLusCouleur ?? DEFAULT_UNREAD_COLOR)
      // The Vue renderer keeps the story mounted when a global changes: the key remounts it for another scenario,
      // so that label lists measure the labels again and creation panels take the color of the scenario.
      return {
        components: { story },
        setup: () => {
          provide(UNREAD_VARIANT_KEY, computed(() => context.globals.nonLus ?? DEFAULT_UNREAD_VARIANT))
          return { globals: context.globals }
        },
        template: '<story :key="globals.etiquettes" />',
      }
    },
  ],
  parameters: {
    options: {
      storySort: {
        method: 'alphabetical',
        locales: 'fr-FR',
        order: [
          'Système de design',
          [
            'Introduction',
            'DDR',
          ],
          'Fondations',
          'Éléments',
          [
            'Génériques',
            'ATS',
          ],
          'Compositions',
          [
            'Layout',
            'Génériques',
            'ATS',
          ],
        ],
      },
    },
  },
}

export default preview
