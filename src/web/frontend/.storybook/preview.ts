import type { Preview } from '@storybook/vue3'
import { setup } from '@storybook/vue3'
import { createMemoryHistory, createRouter } from 'vue-router'
import '../src/app/icons'
import '../src/styles/index.css'
import './storybook.css'

const storybookRouter = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/:pathMatch(.*)*', component: { template: '<div />' } }],
})

setup((app) => {
  app.use(storybookRouter)
})

function applyTheme(theme: string) {
  localStorage.setItem('csp_color_mode', theme)
  document.documentElement.setAttribute('data-fr-theme', theme)
}

function applyShape(shape: string) {
  if (shape === 'rounded') {
    document.documentElement.setAttribute('data-csp-shape', shape)
  }
  else {
    document.documentElement.removeAttribute('data-csp-shape')
  }
}

const preview: Preview = {
  initialGlobals: {
    theme: 'light',
    shape: 'rule',
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
    shape: {
      description: 'Rayons',
      toolbar: {
        title: 'Rayons',
        icon: 'component',
        items: [
          { value: 'rule', title: 'Règle' },
          { value: 'rounded', title: 'Arrondi léger' },
        ],
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (story, context) => {
      applyTheme(context.globals.theme ?? 'light')
      applyShape(context.globals.shape ?? 'rule')
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
