import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useReturnTo } from './useReturnTo'

const routes = [
  { path: '/', component: { template: '<div />' } },
  { path: '/parent', name: 'parent', component: { template: '<div />' } },
  { path: '/parent/child', name: 'child', component: { template: '<div />' } },
]

async function mountAt(paths: string[]) {
  window.history.replaceState(null, '', '/')
  const router = createRouter({ history: createWebHistory(), routes })
  await router.replace(paths[0]!)
  for (const path of paths.slice(1))
    await router.push(path)

  let returnTo!: () => void
  mount(defineComponent({
    setup() {
      returnTo = useReturnTo(() => ({ name: 'parent' }))
      return () => h('div')
    },
  }), { global: { plugins: [router] } })

  return { router, returnTo }
}

describe('useReturnTo', () => {
  it('goes back when the child was reached from another page', async () => {
    const { router, returnTo } = await mountAt(['/parent', '/parent/child'])
    const back = vi.spyOn(router, 'back')

    returnTo()

    expect(back).toHaveBeenCalled()
  })

  it('replaces the address with the fallback when opened directly', async () => {
    const { router, returnTo } = await mountAt(['/parent/child'])

    returnTo()
    await router.isReady()
    await vi.waitFor(() => expect(router.currentRoute.value.name).toBe('parent'))
  })
})
