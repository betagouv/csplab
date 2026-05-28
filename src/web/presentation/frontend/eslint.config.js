import antfu from '@antfu/eslint-config'
import storybook from 'eslint-plugin-storybook'

export default antfu({
  vue: true,
  typescript: true,
  ignores: ['node_modules/', 'dist/', '../static/frontend/', 'storybook-static/'],
}).append(...storybook.configs['flat/recommended'])
