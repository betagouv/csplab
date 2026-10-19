import { createRequire } from 'node:module'
import { RuleTester } from 'eslint'
import { describe, it } from 'vitest'
import rule from './no-hard-coded-color.mjs'

// vue-eslint-parser comes with @antfu/eslint-config, the shared configuration of the project
const vueParser = createRequire(createRequire(import.meta.url).resolve('@antfu/eslint-config'))('vue-eslint-parser')

RuleTester.describe = describe
RuleTester.it = it

const tester = new RuleTester({ languageOptions: { parser: vueParser, ecmaVersion: 'latest', sourceType: 'module' } })

function error(color, line, column) {
  return { messageId: 'hardCodedColor', data: { color }, line, column }
}

tester.run('no-hard-coded-color', rule, {
  valid: [
    {
      name: 'palette keys, links, comments and CSS strings',
      filename: 'CspEssai.vue',
      code: `<script setup>
const props = withDefaults(defineProps(), { color: 'grey' })
const link = { href: '#add' }
</script>

<template>
  <a href="#add">Ancre</a>
  <a :href="'#add'">Ancre</a>
  <CspLabel color="grey" />
  <CspLabel :color="actif ? 'red' : 'blue'" />
  <span :style="{ '--csp-label-dot': paletteVar('red', 'dot') }">#1</span>
</template>

<style scoped>
/* white disc */
.white-text::before {
  content: "Gold #abc";
  color: var(--csp-label-text);
  background-color: color-mix(in srgb, currentColor 12%, transparent);
}
</style>
`,
    },
    {
      name: 'a module of the palette',
      filename: 'etiquettes.ts',
      code: `export const DEFAULT = { color: 'blue', url: '#abc' }`,
    },
  ],
  invalid: [
    {
      name: 'hex code and color function in the script',
      filename: 'CspEssai.vue',
      code: `<script setup>
const fallback = '#ffcc00'
const shade = \`rgb(0 0 0 / \${alpha}%)\`
</script>
`,
      errors: [error('#ffcc00', 2, 19), error('rgb()', 3, 16)],
    },
    {
      name: 'color names in a style object of the script',
      filename: 'CspEssai.vue',
      code: `<script setup>
const style = { color: 'white', backgroundColor: 'red' }
</script>
`,
      errors: [error('white', 2, 25), error('red', 2, 51)],
    },
    {
      name: 'style attribute, :style binding with conditions and other attributes',
      filename: 'CspEssai.vue',
      code: `<template>
  <span style="color: white; background: #123456" />
  <span :style="{ borderColor: actif ? 'red' : 'blue', color: actif && 'black' }" />
  <span data-color="#abc" />
</template>
`,
      errors: [
        error('white', 2, 23),
        error('#123456', 2, 42),
        error('red', 3, 41),
        error('blue', 3, 49),
        error('black', 3, 73),
        error('#abc', 4, 21),
      ],
    },
    {
      name: 'each color of the style block at its line',
      filename: 'CspEssai.vue',
      code: `<style scoped>
.label {
  background: white;
  border: 1px solid gold;
  color: color-mix(in srgb, red 20%, transparent);
  outline-color: rgb(0 0 0);
}
</style>
`,
      errors: [error('white', 3, 15), error('gold', 4, 21), error('red', 5, 29), error('rgb()', 6, 18)],
    },
  ],
})
