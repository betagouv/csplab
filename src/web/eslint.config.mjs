import { readdirSync } from 'node:fs'
import antfu from '@antfu/eslint-config'
import storybook from 'eslint-plugin-storybook'
import noHardCodedColor from './frontend/lint/no-hard-coded-color.mjs'

const SRC = 'frontend/src'
const TESTS = [`${SRC}/**/*.test.ts`]

function subfolders(path) {
  return readdirSync(new URL(path, import.meta.url), { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
}

const FEATURES = subfolders(`./${SRC}/features`)
const ROOT_FOLDERS = subfolders(`./${SRC}`).filter(folder => !['features', 'app', 'router', 'test'].includes(folder))

// Components that read their colors from the palette variables of styles/palette.css
const PALETTE_COMPONENTS = [
  `${SRC}/components/base/CspLabel/**`,
  `${SRC}/components/base/CspAvatar/**`,
  `${SRC}/**/*[Ee]tiquette*.{ts,vue}`,
  `${SRC}/app/prototypes/ColorField.vue`,
]

const FEATURE_DEPENDENCIES = {
  'candidatures': ['recrutements', 'etapes-recrutement', 'messages'],
  'etapes-recrutement': ['recrutements'],
  'organismes': ['agents'],
  'recrutements': ['agents'],
  'equipe-recrutement': ['agents'],
}

function assertAcyclic(graph) {
  const done = new Set()
  function visit(feature, path) {
    if (path.includes(feature)) {
      throw new Error(`FEATURE_DEPENDENCIES has a cycle: ${[...path, feature].join(' → ')}`)
    }
    if (done.has(feature)) {
      return
    }
    for (const dependency of graph[feature] ?? []) {
      visit(dependency, [...path, feature])
    }
    done.add(feature)
  }
  Object.keys(graph).forEach(feature => visit(feature, []))
}

assertAcyclic(FEATURE_DEPENDENCIES)

function restrictImports(files, patterns) {
  return {
    files,
    ignores: TESTS,
    rules: {
      'no-restricted-imports': ['error', { patterns }],
    },
  }
}

function restrictFeatureImports(feature) {
  const dependencies = FEATURE_DEPENDENCIES[feature] ?? []
  const otherFeatures = FEATURES.filter(other => other !== feature)
  return restrictImports([`${SRC}/features/${feature}/**`], [
    {
      regex: `^@/features/(?!(${[feature, ...dependencies].join('|')})/)`,
      message: dependencies.length > 0
        ? `${feature} imports no feature other than ${dependencies.join(', ')} (FEATURE_DEPENDENCIES).`
        : `${feature} imports no other feature (FEATURE_DEPENDENCIES).`,
    },
    {
      regex: `^(\\.\\./)+(features/)?(${otherFeatures.join('|')})/`,
      message: 'An import from another feature uses the @/features/ alias.',
    },
  ])
}

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
  {
    files: PALETTE_COMPONENTS,
    plugins: { csp: { rules: { 'no-hard-coded-color': noHardCodedColor } } },
    rules: { 'csp/no-hard-coded-color': 'error' },
  },
  ...FEATURES.map(restrictFeatureImports),
  restrictImports(ROOT_FOLDERS.map(folder => `${SRC}/${folder}/**`), [
    { regex: '^(@/|(\\.\\./)+)features/', message: 'Root folders import no feature; router/ and app/ may.' },
  ]),
  storybook.configs['flat/recommended'],
)
