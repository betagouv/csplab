import type { Preview } from '@storybook/vue3'
import { PiniaColada } from '@pinia/colada'
import { setup } from '@storybook/vue3'
import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { sb } from 'storybook/test'
import { createMemoryHistory, createRouter } from 'vue-router'
import { applyUiTheme, UI_THEMES } from '../src/composables/ui/useUiTheme'
import { routes } from '../src/router/routes'
import { applyScenario, DEFAULT_SCENARIO, SCENARIOS } from '../src/styles/etiquettes/scenarios'
import '../src/app/icons'
import '../src/styles/index.css'
import './storybook.css'

// Demo data for the prototype screens: each module is replaced by the file of the same name in its __mocks__ folder.
sb.mock('../src/api/utilisateur.ts')
sb.mock('../src/features/candidatures/api.ts')
sb.mock('../src/features/equipe-recrutement/api.ts')
sb.mock('../src/features/etapes-recrutement/api.ts')
sb.mock('../src/features/messages/api.ts')
sb.mock('../src/features/organismes/api.ts')
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
const COMPACT = 'compact'
const COMFORTABLE = 'comfortable'
const LARGE = 'large'

function applyDensity(density: string) {
  if (density === COMFORTABLE || density === LARGE) {
    document.documentElement.setAttribute('data-csp-density', density)
  }
  else {
    document.documentElement.removeAttribute('data-csp-density')
  }
}

const preview: Preview = {
  initialGlobals: {
    theme: 'light',
    interfaceTheme: 'kit',
    density: COMPACT,
    etiquettes: DEFAULT_SCENARIO ?? NO_SCENARIO,
  },
  globalTypes: {
    theme: {
      description: 'Thème clair ou sombre du DSFR',
      toolbar: {
        title: 'Thème clair ou sombre',
        icon: 'contrast',
        items: [
          { value: 'light', title: 'Clair', icon: 'sun' },
          { value: 'dark', title: 'Sombre', icon: 'moon' },
        ],
        dynamicTitle: true,
      },
    },
    interfaceTheme: {
      description: 'Thème d’interface',
      toolbar: {
        title: 'Thème',
        icon: 'component',
        items: UI_THEMES.map(({ id, name }) => ({ value: id, title: name })),
        dynamicTitle: true,
      },
    },
    density: {
      description: 'Densité',
      toolbar: {
        title: 'Densité',
        icon: 'grow',
        items: [
          { value: COMPACT, title: 'Compacte, texte à 14 px' },
          { value: COMFORTABLE, title: 'Confortable, texte à 16 px' },
          { value: LARGE, title: 'Grande, texte à 18 px' },
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
  },
  decorators: [
    (story, context) => {
      applyTheme(context.globals.theme ?? 'light')
      applyUiTheme(context.globals.interfaceTheme)
      applyDensity(context.globals.density ?? COMPACT)
      applyScenario(document.documentElement, context.globals.etiquettes)
      // The Vue renderer keeps the story mounted when a global changes: the key remounts it for another theme, density or scenario,
      // so that label lists measure the labels again and creation panels take the color of the scenario.
      return {
        components: { story },
        setup: () => ({ globals: context.globals }),
        template: '<story :key="[globals.interfaceTheme, globals.density, globals.etiquettes].join()" />',
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
