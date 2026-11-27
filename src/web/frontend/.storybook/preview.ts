import type { Preview } from '@storybook/vue3'
import { setup } from '@storybook/vue3'
import { createMemoryHistory, createRouter } from 'vue-router'
import { applyUiSettings, UI_DENSITIES, UI_SHAPES } from '../src/styles/uiSettings'
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

function applyColorMode(colorMode: string) {
  localStorage.setItem('csp_color_mode', colorMode)
  document.documentElement.setAttribute('data-fr-theme', colorMode)
}

const SHAPE_TITLES: Record<typeof UI_SHAPES[number], string> = { dsfr: 'DSFR strict', rounded: 'Arrondi' }
const DENSITY_TITLES: Record<typeof UI_DENSITIES[number], string> = { standard: 'Standard', compact: 'Compacte', comfortable: 'Confortable' }

const preview: Preview = {
  initialGlobals: {
    theme: 'light',
    shape: UI_SHAPES[0],
    density: UI_DENSITIES[0],
  },
  globalTypes: {
    theme: {
      description: 'Mode de couleur',
      toolbar: {
        title: 'Mode de couleur',
        icon: 'contrast',
        items: [
          { value: 'light', title: 'Clair', icon: 'sun' },
          { value: 'dark', title: 'Sombre', icon: 'moon' },
        ],
        dynamicTitle: true,
      },
    },
    shape: {
      description: 'Forme',
      toolbar: {
        title: 'Forme',
        icon: 'component',
        items: UI_SHAPES.map(value => ({ value, title: SHAPE_TITLES[value] })),
        dynamicTitle: true,
      },
    },
    density: {
      description: 'Densité',
      toolbar: {
        title: 'Densité',
        icon: 'grow',
        items: UI_DENSITIES.map(value => ({ value, title: DENSITY_TITLES[value] })),
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (story, context) => {
      applyColorMode(context.globals.theme ?? 'light')
      applyUiSettings({ shape: context.globals.shape ?? UI_SHAPES[0], density: context.globals.density ?? UI_DENSITIES[0] })
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
