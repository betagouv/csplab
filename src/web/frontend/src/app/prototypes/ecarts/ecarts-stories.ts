import type { Decorator } from '@storybook/vue3-vite'
import { onUnmounted } from 'vue'
import { below } from '@/styles/breakpoints'

const ECART_ATTRIBUTE = 'data-ecart'

export function withEcart(value?: string): Decorator {
  return story => ({
    components: { story },
    setup() {
      const root = document.documentElement
      if (value) {
        root.setAttribute(ECART_ATTRIBUTE, value)
      }
      else {
        root.removeAttribute(ECART_ATTRIBUTE)
      }
      onUnmounted(() => root.removeAttribute(ECART_ATTRIBUTE))
    },
    template: '<story />',
  })
}

// The sidebar switches to its mobile drawer below the lg breakpoint, wider than a board column
export const withDesktopSidebar: Decorator = story => ({
  components: { story },
  setup() {
    const original = window.matchMedia
    const mobileQuery = below('lg')
    window.matchMedia = query => original.call(window, query === mobileQuery ? '(width < 0px)' : query)
    onUnmounted(() => {
      window.matchMedia = original
    })
  },
  template: '<story />',
})
