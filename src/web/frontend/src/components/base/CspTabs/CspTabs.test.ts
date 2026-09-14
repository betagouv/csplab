import { render, within } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h } from 'vue'
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
    const { getAllByRole, getByRole } = render(CspTabs, {
      props: { tabs: TABS, defaultValue: 'a' },
      slots: { a: () => 'Contenu A', b: () => 'Contenu B' },
      global,
    })

    expect(getAllByRole('tab').map(tab => tab.textContent?.trim())).toEqual(['Onglet A', 'Onglet B'])
    expect(getByRole('tabpanel')).toHaveTextContent('Contenu A')
  })

  it('shares the active tab between a detached list and panels', () => {
    const { container } = render(
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

    const header = within(container.querySelector('header')!)
    const main = within(container.querySelector('main')!)
    expect(header.getByRole('tab', { name: 'Onglet A', selected: true })).toBeInTheDocument()
    expect(main.getByRole('tabpanel')).toHaveTextContent('Contenu A')
  })
})
