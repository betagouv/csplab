// Reports each color written in a label component, at its own position: a hex code or a color function
// anywhere in the script, the template and the style block, and a color name in a CSS value: a style block,
// a style attribute, a :style binding or a style object of the script. The colors of these components come
// from the palette variables.
import { PALETTE_COLORS } from '../src/styles/palette.ts'

const COLOR_NAMES = `aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown
  burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod
  darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
  darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue
  firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew
  hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
  lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray
  lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid
  mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream
  mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen
  paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue
  saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen
  steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen`.split(/\s+/)

const HEX = /(?<![&\w])#[\da-f]{3,8}(?![\w-])/gi
const COLOR_FUNCTION = /\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(/gi
const COLOR_NAME = new RegExp(`(?<![\\w-])(?:${COLOR_NAMES.join('|')})(?![\\w-])`, 'gi')
// The value of a CSS declaration; a selector ends with { and stays out
const DECLARATION = /[\w-]+\s*:([^;{}]*)(?=[;}]|$)/g
// Comments and quoted strings of CSS, which hold no color
const CSS_TEXT = /\/\*[\s\S]*?\*\/|\/\/[^\n]*|"[^"\n]*"|'[^'\n]*'/g
const LINK_KEYS = new Set(['href', 'src', 'url', 'to'])
// Keys of a style object whose value is a color; a palette component also takes a palette key in a color prop
const STYLE_COLOR_KEYS = new Set(['color', 'background', 'backgroundColor', 'borderColor', 'outlineColor', 'fill', 'stroke'])
const PALETTE_KEYS = new Set(PALETTE_COLORS)

function find(text, patterns) {
  return patterns.flatMap(pattern => [...text.matchAll(pattern)].map(match => ({ index: match.index, color: match[0] })))
}

function findInCss(css) {
  const code = css.replace(CSS_TEXT, text => ' '.repeat(text.length))
  return [...code.matchAll(DECLARATION)].flatMap((declaration) => {
    const start = declaration.index + declaration[0].length - declaration[1].length
    return find(declaration[1], [HEX, COLOR_FUNCTION, COLOR_NAME]).map(found => ({ ...found, index: start + found.index }))
  })
}

// The expression that holds a value, past the branches of a condition: actif ? 'red' : 'blue', actif && 'black'
function valueExpression(node) {
  let current = node
  while (current.parent?.type === 'LogicalExpression' || (current.parent?.type === 'ConditionalExpression' && current.parent.test !== current)) {
    current = current.parent
  }
  return current
}

function propertyKey(expression) {
  const { parent } = expression
  return parent?.type === 'Property' && parent.value === expression ? (parent.key.name ?? parent.key.value) : undefined
}

function boundAttribute(node) {
  for (let ancestor = node.parent; ancestor; ancestor = ancestor.parent) {
    if (ancestor.type === 'VAttribute') {
      return ancestor.directive && ancestor.key.name.name === 'bind' ? ancestor.key.argument?.name : undefined
    }
  }
  return undefined
}

export default {
  meta: {
    type: 'problem',
    docs: { description: 'Refuse a color written in a label component' },
    messages: {
      hardCodedColor: 'Color {{color}} written in a label component: read it from the palette, paletteVar() or var(--csp-palette-*).',
    },
    schema: [],
  },
  create(context) {
    const { sourceCode } = context

    function report(found, offset) {
      const start = offset + found.index
      context.report({
        loc: { start: sourceCode.getLocFromIndex(start), end: sourceCode.getLocFromIndex(start + found.color.length) },
        messageId: 'hardCodedColor',
        data: { color: found.color.endsWith('(') ? `${found.color})` : found.color },
      })
    }

    // text: source text of a string literal or of a template part, starting at offset
    function check(node, text, offset, attribute) {
      const expression = valueExpression(node.type === 'TemplateElement' ? node.parent : node)
      const key = propertyKey(expression)
      if (LINK_KEYS.has(key) || LINK_KEYS.has(attribute)) {
        return
      }
      const isStyleBinding = attribute === 'style' && (key !== undefined || expression.parent?.type === 'VExpressionContainer')
      const isStyleObject = STYLE_COLOR_KEYS.has(key)
      const names = isStyleBinding || isStyleObject
      find(text, names ? [HEX, COLOR_FUNCTION, COLOR_NAME] : [HEX, COLOR_FUNCTION])
        .filter(found => isStyleBinding || key !== 'color' || !PALETTE_KEYS.has(found.color.toLowerCase()))
        .forEach(found => report(found, offset))
    }

    function checkLiteral(node, attribute) {
      if (typeof node.value === 'string') {
        check(node, node.raw, node.range[0], attribute)
      }
    }

    function checkTemplateElement(node, attribute) {
      check(node, node.value.raw, node.range[0] + 1, attribute)
    }

    function checkStyleBlocks() {
      const fragment = sourceCode.parserServices?.getDocumentFragment?.()
      fragment?.children
        .filter(element => element.type === 'VElement' && element.name === 'style')
        .flatMap(element => element.children.filter(child => child.type === 'VText'))
        .forEach(text => findInCss(text.value).forEach(found => report(found, text.range[0])))
    }

    const scriptVisitor = {
      'Literal': node => checkLiteral(node),
      'TemplateElement': node => checkTemplateElement(node),
      'Program:exit': checkStyleBlocks,
    }
    if (!sourceCode.parserServices?.defineTemplateBodyVisitor) {
      return scriptVisitor
    }
    return sourceCode.parserServices.defineTemplateBodyVisitor({
      VLiteral(node) {
        const attribute = node.parent
        if (attribute.directive || LINK_KEYS.has(attribute.key.name)) {
          return
        }
        const offset = node.range[0] + (/["']/.test(sourceCode.text[node.range[0]]) ? 1 : 0)
        const found = attribute.key.name === 'style' ? findInCss(node.value) : find(node.value, [HEX, COLOR_FUNCTION])
        found.forEach(color => report(color, offset))
      },
      Literal: node => checkLiteral(node, boundAttribute(node)),
      TemplateElement: node => checkTemplateElement(node, boundAttribute(node)),
    }, scriptVisitor)
  },
}
