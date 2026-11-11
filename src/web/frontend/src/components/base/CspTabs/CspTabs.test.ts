import { render, screen, within } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h, onMounted } from 'vue'
import { setupUser } from '@/test/render'
import CspTabs from './CspTabs.vue'
import CspTabsList from './CspTabsList.vue'
import CspTabsPanels from './CspTabsPanels.vue'

const CspIconStub = defineComponent({
  name: 'CspIcon',
  props: { name: { type: String, required: true } },
  setup: props => () => h('i', { 'class': 'csp-icon', 'data-icon': props.name }),
})

const global = { stubs: { CspIcon: CspIconStub } }

const TABS = [
  { value: 'a', label: 'Onglet A' },
  { value: 'b', label: 'Onglet B' },
]

describe('cspTabs', () => {
  it('renders one tab per item and the active panel', () => {
    render(CspTabs, {
      props: { tabs: TABS, defaultValue: 'a' },
      slots: { a: () => 'Contenu A', b: () => 'Contenu B' },
      global,
    })

    expect(screen.getAllByRole('tab').map(tab => tab.textContent?.trim())).toEqual(['Onglet A', 'Onglet B'])
    expect(screen.getByRole('tabpanel')).toHaveTextContent('Contenu A')
  })

  it('shares the active tab between a detached list and panels', () => {
    render(
      defineComponent({
        setup() {
          return () =>
            h(CspTabs, { defaultValue: 'a' }, () => [
              h('header', [h(CspTabsList, { tabs: TABS })]),
              h('main', [h(CspTabsPanels, { tabs: TABS }, { a: () => 'Contenu A', b: () => 'Contenu B' })]),
            ])
        },
      }),
      { global },
    )

    const header = within(screen.getByRole('banner'))
    const main = within(screen.getByRole('main'))
    expect(header.getByRole('tab', { name: 'Onglet A', selected: true })).toBeInTheDocument()
    expect(main.getByRole('tabpanel')).toHaveTextContent('Contenu A')
  })

  it('keeps a shared panel mounted and controlled by the selected tab', async () => {
    let mounts = 0
    const SharedContent = defineComponent({
      setup() {
        onMounted(() => {
          mounts++
        })
        return () => 'Contenu partagé'
      },
    })
    const user = setupUser()
    render(
      defineComponent({
        setup() {
          return () =>
            h(CspTabs, { defaultValue: 'a' }, () => [
              h(CspTabsList, { tabs: TABS }),
              h(CspTabsPanels, { tabs: TABS }, { default: () => h(SharedContent) }),
            ])
        },
      }),
      { global },
    )

    await user.click(screen.getByRole('tab', { name: 'Onglet B' }))

    expect(screen.getByRole('tab', { name: 'Onglet B', selected: true })).toHaveAttribute('aria-controls', screen.getByRole('tabpanel').id)
    expect(mounts).toBe(1)
  })
})
