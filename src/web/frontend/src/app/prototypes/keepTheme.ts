import type { Decorator } from '@storybook/vue3-vite'
import { onBeforeUnmount } from 'vue'

// A deck loads several stories at once, and the application reads its color mode from the localStorage they share
// and from the system preference: the decorator puts the theme of the story back when the application changes it.
export const keepTheme: Decorator = (story, context) => ({
  components: { story },
  setup() {
    const root = document.documentElement
    const observer = new MutationObserver(() => {
      if (root.getAttribute('data-fr-theme') !== context.globals.theme) {
        root.setAttribute('data-fr-theme', context.globals.theme)
      }
    })
    observer.observe(root, { attributes: true, attributeFilter: ['data-fr-theme'] })
    onBeforeUnmount(() => observer.disconnect())
  },
  template: '<story />',
})
