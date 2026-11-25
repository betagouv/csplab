import { dirname, resolve } from 'node:path'

// no-restricted-syntax compares the written path; this rule resolves a relative path such as '../api' to its feature.
export default {
  meta: {
    type: 'problem',
    schema: [{ type: 'array', items: { type: 'string' } }],
    messages: { handlers: 'Answer the {{feature}} API with server.use() and a factory of @/test/handlers/{{feature}}.' },
  },
  create(context) {
    const [features] = context.options
    return {
      'CallExpression[callee.object.name="vi"][callee.property.name="mock"]': (node) => {
        const source = node.arguments[0]?.value
        if (typeof source !== 'string') {
          return
        }
        const module = source.startsWith('.') ? resolve(dirname(context.filename), source) : source
        const feature = features.find(name => module.endsWith(`/features/${name}/api`))
        if (feature) {
          context.report({ node, messageId: 'handlers', data: { feature } })
        }
      },
    }
  },
}
