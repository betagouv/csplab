import type { MaybeRefOrGetter } from 'vue'
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
  { path: '/fiche/:id', name: 'fiche-liste', component: stub, meta: { tab: 'liste' } },
  { path: '/fiche/:id/archives', name: 'fiche-archives', component: stub, meta: { tab: 'archives' } },
]

const ROUTE_NAMES_FICHE: Record<Onglet, string> = {
  liste: 'fiche-liste',
  archives: 'fiche-archives',
}

async function mountRouteTab(
  path: string,
  routeNames: MaybeRefOrGetter<Record<Onglet, string>> = ROUTE_NAMES,
) {
  const router = createRouter({ history: createMemoryHistory(), routes: testRoutes })
  await router.push(path)

  let tab!: ReturnType<typeof useRouteTab<Onglet>>

  mount(defineComponent({
    setup() {
      tab = useRouteTab(routeNames, 'liste')
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

  it('keeps the route params when switching tab', async () => {
    const { tab, router } = await mountRouteTab('/fiche/42', ROUTE_NAMES_FICHE)

    tab.value = 'archives'
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe('/fiche/42/archives'))
  })

  it('resolves the route names from a getter, re-read on each navigation', async () => {
    const maps = { demo: ROUTE_NAMES, fiche: ROUTE_NAMES_FICHE }
    let current: keyof typeof maps = 'fiche'
    const { tab, router } = await mountRouteTab('/fiche/42', () => maps[current])

    tab.value = 'archives'
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe('/fiche/42/archives'))

    current = 'demo'
    tab.value = 'liste'
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe('/demo'))
  })
})
