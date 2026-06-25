import { mount } from '@vue/test-utils'
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

describe('cspTabs: monolithic usage', () => {
  it('renders the tab list and forwards the active panel slot', () => {
    const wrapper = mount(CspTabs, {
      props: { tabs: TABS, defaultValue: 'a' },
      slots: {
        a: () => 'Contenu A',
        b: () => 'Contenu B',
      },
      global,
    })

    const triggers = wrapper.findAll('.csp-tabs__trigger')
    expect(triggers).toHaveLength(2)
    expect(triggers[0].text()).toBe('Onglet A')
    expect(wrapper.text()).toContain('Contenu A')
  })
})

describe('cspTabs: composed usage (list and panels in separate regions)', () => {
  it('shares active state between a detached list and panels', () => {
    const wrapper = mount(
      defineComponent({
        components: { CspTabs, CspTabsList, CspTabsPanels },
        setup() {
          return () =>
            h(CspTabs, { defaultValue: 'a' }, () => [
              h('header', [h(CspTabsList, { tabs: TABS })]),
              h('main', [
                h(CspTabsPanels, { tabs: TABS }, {
                  a: () => 'Contenu A',
                  b: () => 'Contenu B',
                }),
              ]),
            ])
        },
      }),
      { global },
    )

    expect(wrapper.find('header .csp-tabs__list').exists()).toBe(true)
    expect(wrapper.find('main .csp-tabs__panels').exists()).toBe(true)
    expect(wrapper.text()).toContain('Contenu A')
  })
})
