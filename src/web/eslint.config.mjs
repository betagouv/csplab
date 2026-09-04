import antfu from '@antfu/eslint-config'
import storybook from 'eslint-plugin-storybook'

export default antfu(
  {
    formatters: {
      css: true,
    },
    vue: true,
    typescript: true,
    toml: false,
    pnpm: false,
    ignores: [
      '.venv/',
      'node_modules/',
      'frontend/storybook-static/',
      'frontend/src/types/',
      'presentation/static/api/',
      'presentation/static/css/**',
      'presentation/static/js/**',
      'tests/',
    ],
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
