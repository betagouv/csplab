import type { Preview } from '@storybook/vue3'
import { setup } from '@storybook/vue3'
import { createMemoryHistory, createRouter } from 'vue-router'
import { applyUiSettings } from '../src/styles/uiSettings'
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

const preview: Preview = {
  initialGlobals: {
    theme: 'light',
    shape: 'dsfr',
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
      description: 'Thème de rayons',
      toolbar: {
        title: 'Thème de rayons',
        icon: 'component',
        items: [
          { value: 'dsfr', title: 'DSFR strict' },
          { value: 'rounded', title: 'Arrondi' },
        ],
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (story, context) => {
      applyTheme(context.globals.theme ?? 'light')
      applyUiSettings({ shape: context.globals.shape ?? 'dsfr', density: 'standard' })
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
