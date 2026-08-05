import type { RouteRecordRaw } from 'vue-router'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { useRouteTab } from './useRouteTab'

type Onglet = 'liste' | 'archives'

const ROUTE_NAMES: Record<Onglet, string> = {
  liste: 'demo-liste',
  archives: 'demo-archives',
}

const stub = defineComponent({ setup: () => () => h('div') })

const testRoutes: RouteRecordRaw[] = [
  { path: '/demo', name: ROUTE_NAMES.liste, component: stub, meta: { tab: 'liste' } },
  { path: '/demo/archives', name: ROUTE_NAMES.archives, component: stub, meta: { tab: 'archives' } },
  { path: '/ailleurs', name: 'ailleurs', component: stub },
  { path: '/mal-declare', name: 'mal-declare', component: stub, meta: { tab: 'onglet-inconnu' } },
]

async function mountRouteTab(path: string) {
  const router = createRouter({ history: createMemoryHistory(), routes: testRoutes })
  await router.push(path)

  let tab!: ReturnType<typeof useRouteTab<Onglet>>

  mount(defineComponent({
    setup() {
      tab = useRouteTab(ROUTE_NAMES, 'liste')
      return () => h('div')
    },
  }), {
    global: { plugins: [router] },
  })

  return { tab, router }
}

describe('useRouteTab', () => {
  it('reads the tab from the current route', async () => {
    const { tab } = await mountRouteTab('/demo/archives')
    expect(tab.value).toBe('archives')
  })

  it('navigates when the tab is set', async () => {
    const { tab, router } = await mountRouteTab('/demo')

    tab.value = 'archives'
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe('/demo/archives'))

    expect(tab.value).toBe('archives')
  })

  it('restores the previous tab on browser back', async () => {
    const { tab, router } = await mountRouteTab('/demo')

    tab.value = 'archives'
    await vi.waitFor(() => expect(tab.value).toBe('archives'))

    router.back()
    await vi.waitFor(() => expect(tab.value).toBe('liste'))

    expect(router.currentRoute.value.path).toBe('/demo')
  })

  it.each([
    ['the route declares no tab', '/ailleurs'],
    ['the route declares an unknown tab', '/mal-declare'],
  ])('falls back to the default tab when %s', async (_, path) => {
    const { tab } = await mountRouteTab(path)
    expect(tab.value).toBe('liste')
  })
})
