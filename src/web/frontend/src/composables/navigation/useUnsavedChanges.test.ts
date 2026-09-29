import { render } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { createMemoryHistory, createRouter, RouterView } from 'vue-router'
import { useUnsavedChanges, useUnsavedChangesGuard } from './useUnsavedChanges'

async function mountGuard() {
  const text = ref('')
  let guard!: ReturnType<typeof useUnsavedChangesGuard>

  const Input = defineComponent({
    setup() {
      useUnsavedChanges(() => text.value !== '', () => {
        text.value = ''
      })
      return () => h('textarea')
    },
  })

  const Page = defineComponent({
    setup() {
      guard = useUnsavedChangesGuard({ ignore: (to, from) => to.params.id === from.params.id })
      return () => h(Input)
    },
  })

  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/fiche/:id', component: Page },
      { path: '/fiche/:id/notes', component: Page },
      { path: '/ailleurs', component: defineComponent({ setup: () => () => h('div') }) },
    ],
  })
  await router.push('/fiche/1')
  render(RouterView, { global: { plugins: [router] } })

  return { router, text, guard }
}

describe('useUnsavedChanges', () => {
  it('lets the navigation through when nothing is typed', async () => {
    const { router, guard } = await mountGuard()

    await router.push('/fiche/2')

    expect(router.currentRoute.value.path).toBe('/fiche/2')
    expect(guard.isConfirming.value).toBe(false)
  })

  it('holds the navigation until the user leaves, then discards the input', async () => {
    const { router, text, guard } = await mountGuard()
    text.value = 'Brouillon'

    const navigation = router.push('/ailleurs')
    await vi.waitFor(() => expect(guard.isConfirming.value).toBe(true))
    expect(router.currentRoute.value.path).toBe('/fiche/1')

    guard.leave()
    await navigation

    expect(router.currentRoute.value.path).toBe('/ailleurs')
    expect(text.value).toBe('')
  })

  it('cancels the navigation and keeps the input when the user keeps editing', async () => {
    const { router, text, guard } = await mountGuard()
    text.value = 'Brouillon'

    const navigation = router.push('/ailleurs')
    await vi.waitFor(() => expect(guard.isConfirming.value).toBe(true))
    guard.keepEditing()
    await navigation

    expect(router.currentRoute.value.path).toBe('/fiche/1')
    expect(text.value).toBe('Brouillon')
    expect(guard.isConfirming.value).toBe(false)
  })

  it('ignores the navigations the guard is told to ignore', async () => {
    const { router, text, guard } = await mountGuard()
    text.value = 'Brouillon'

    await router.push('/fiche/1/notes')

    expect(router.currentRoute.value.path).toBe('/fiche/1/notes')
    expect(guard.isConfirming.value).toBe(false)
    expect(text.value).toBe('Brouillon')
  })

  it('asks the browser to warn before unloading the page while an input is typed', async () => {
    const { text } = await mountGuard()

    const clean = new Event('beforeunload', { cancelable: true })
    window.dispatchEvent(clean)
    expect(clean.defaultPrevented).toBe(false)

    text.value = 'Brouillon'
    const dirty = new Event('beforeunload', { cancelable: true })
    window.dispatchEvent(dirty)
    expect(dirty.defaultPrevented).toBe(true)
  })
})
