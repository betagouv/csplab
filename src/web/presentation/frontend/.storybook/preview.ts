import type { Preview } from '@storybook/vue3'
import { setup } from '@storybook/vue3'
import { createMemoryHistory, createRouter } from 'vue-router'
import '../src/styles/index.css'

const storybookRouter = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/:pathMatch(.*)*', component: { template: '<div />' } }],
})

setup((app) => {
  app.use(storybookRouter)
})

const preview: Preview = {
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
