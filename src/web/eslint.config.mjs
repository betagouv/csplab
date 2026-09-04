import antfu from '@antfu/eslint-config'

export default antfu({
  formatters: {
    css: true,
  },
  ignores: [
    '.venv/',
    'node_modules/',
    'frontend/',
    'presentation/static/css/**',
    'presentation/static/js/**',
  ],
})
