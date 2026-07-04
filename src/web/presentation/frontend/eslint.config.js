import antfu from '@antfu/eslint-config'
import storybook from 'eslint-plugin-storybook'

export default antfu(
  {
    formatters: {
      css: true,
    },
    vue: true,
    typescript: true,
    ignores: ['node_modules/', 'dist/', 'storybook-static/', 'src/types/'],
  },
  {
    files: ['**/*.vue'],
    rules: {
      'vue/max-attributes-per-line': [
        'error',
        {
          singleline: {
            max: 1,
          },
          multiline: {
            max: 1,
          },
        },
      ],
    },
  },
  storybook.configs['flat/recommended'],
)
