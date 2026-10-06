import antfu from '@antfu/eslint-config'
import storybook from 'eslint-plugin-storybook'

export default antfu(
  {
    formatters: {
      css: true,
    },
    stylistic: {
      overrides: {
        'antfu/curly': 'off',
        'curly': ['error', 'all'],
        'style/brace-style': ['error', 'stroustrup', { allowSingleLine: false }],
      },
    },
    vue: {
      overrides: {
        'vue/no-restricted-syntax': ['error', 'DebuggerStatement', 'LabeledStatement', 'WithStatement', {
          selector: 'IfStatement > :not(BlockStatement).consequent, IfStatement > :not(BlockStatement, IfStatement).alternate',
          message: 'Wrap the body of if and else in braces.',
        }],
      },
    },
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
