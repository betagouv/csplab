import type { Preview } from '@storybook/vue3'
import { PiniaColada } from '@pinia/colada'
import { setup } from '@storybook/vue3'
import { createHead } from '@unhead/vue/client'
import { mswLoader } from 'msw-storybook-addon/csf3'
import { setupWorker } from 'msw/browser'
import { createPinia } from 'pinia'
import { sb } from 'storybook/test'
import { createMemoryHistory, createRouter } from 'vue-router'
import { recrutementsHandlers } from '../src/features/recrutements/__mocks__/handlers'
import { routes } from '../src/router/routes'
import '../src/app/icons'
import '../src/styles/index.css'
import './storybook.css'

// Demo data for the prototype screens: each module is replaced by the file of the same name in its __mocks__ folder.
sb.mock('../src/api/documents.ts')
sb.mock('../src/api/utilisateur.ts')
sb.mock('../src/features/agents/api.ts')
sb.mock('../src/features/candidatures/api.ts')
sb.mock('../src/features/equipe-recrutement/api.ts')
sb.mock('../src/features/etapes-recrutement/api.ts')
sb.mock('../src/features/messages/api.ts')
sb.mock('../src/features/organismes/api.ts')
sb.mock('../src/features/tags/api.ts')
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

// The recrutements requests are answered by Mock Service Worker. The worker script sits next to iframe.html,
// so the relative URL holds under the subpath of a branch preview.
const startWorker = mswLoader(async () => {
  const worker = setupWorker(...recrutementsHandlers)
  await worker.start({ serviceWorker: { url: './mockServiceWorker.js' }, onUnhandledFrame: 'bypass', quiet: true })
  return worker
})

const preview: Preview = {
  loaders: [startWorker],
  initialGlobals: {
    theme: 'light',
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
  },
  decorators: [
    (story, context) => {
      applyTheme(context.globals.theme ?? 'light')
      return { components: { story }, template: '<story />' }
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
