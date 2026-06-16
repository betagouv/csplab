import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import CspTag from './CspTag.vue'
import CspTagGroup from './CspTagGroup.vue'

const CspIconStub = defineComponent({
  name: 'CspIcon',
  props: { name: { type: String, required: true } },
  setup: props => () => h('i', { 'class': 'csp-icon', 'data-icon': props.name }),
})

const global = { stubs: { CspIcon: CspIconStub } }

describe('cspTag: root element per variant', () => {
  it('static variant renders <p>', () => {
    const wrapper = mount(CspTag, { props: { label: 'Cat' }, global })
    expect(wrapper.element.tagName).toBe('P')
    expect(wrapper.classes()).toContain('csp-tag')
    expect(wrapper.classes()).not.toContain('csp-tag--interactive')
    expect(wrapper.text()).toBe('Cat')
  })

  it('clickable variant with href renders <a href>', () => {
    const wrapper = mount(CspTag, { props: { variant: 'clickable', label: 'Lien', href: '/x' }, global })
    expect(wrapper.element.tagName).toBe('A')
    expect(wrapper.attributes('href')).toBe('/x')
    expect(wrapper.classes()).toContain('csp-tag--interactive')
  })

  it('clickable variant without href renders <button>', () => {
    const wrapper = mount(CspTag, { props: { variant: 'clickable', label: 'Action' }, global })
    expect(wrapper.element.tagName).toBe('BUTTON')
    expect(wrapper.attributes('type')).toBe('button')
  })

  it('disabled clickable with href renders <button>', () => {
    const wrapper = mount(CspTag, { props: { variant: 'clickable', label: 'X', href: '/x', disabled: true }, global })
    expect(wrapper.element.tagName).toBe('BUTTON')
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('dismissible variant renders <button> with cross and derived aria-label', () => {
    const wrapper = mount(CspTag, { props: { variant: 'dismissible', label: 'Vue' }, global })
    expect(wrapper.element.tagName).toBe('BUTTON')
    expect(wrapper.attributes('aria-label')).toBe('Retirer le filtre Vue')
    expect(wrapper.find('.csp-tag__dismiss').exists()).toBe(true)
  })
})

describe('cspTag: icon', () => {
  it('renders icon on a variant that allows it', () => {
    const wrapper = mount(CspTag, { props: { label: 'Cat', icon: 'ri:bookmark-line' }, global })
    const icon = wrapper.find('.csp-tag__icon')
    expect(icon.exists()).toBe(true)
    expect(icon.attributes('data-icon')).toBe('ri:bookmark-line')
  })

  it('dismissible never renders an icon in addition to the cross', () => {
    const wrapper = mount(CspTag, { props: { variant: 'dismissible', label: 'Vue' }, global })
    expect(wrapper.find('.csp-tag__icon').exists()).toBe(false)
    expect(wrapper.find('.csp-tag__dismiss').exists()).toBe(true)
  })
})

describe('cspTag: selectable (standalone Toggle)', () => {
  it('reflects the pressed state and emits update:pressed on click', async () => {
    const wrapper = mount(CspTag, { props: { variant: 'selectable', label: 'F', pressed: false }, global })
    expect(wrapper.attributes('aria-pressed')).toBe('false')
    expect(wrapper.attributes('data-state')).toBe('off')

    await wrapper.trigger('click')
    expect(wrapper.emitted('update:pressed')).toBeTruthy()
    expect(wrapper.emitted('update:pressed')![0]).toEqual([true])
  })

  it('does not emit update:pressed when disabled', async () => {
    const wrapper = mount(CspTag, { props: { variant: 'selectable', label: 'F', disabled: true }, global })
    await wrapper.trigger('click')
    expect(wrapper.emitted('update:pressed')).toBeFalsy()
  })
})

describe('cspTag: dismissible', () => {
  it('emits dismiss on click', async () => {
    const wrapper = mount(CspTag, { props: { variant: 'dismissible', label: 'Vue' }, global })
    await wrapper.trigger('click')
    expect(wrapper.emitted('dismiss')).toHaveLength(1)
  })

  it('prefers an explicit dismissLabel', () => {
    const wrapper = mount(CspTag, { props: { variant: 'dismissible', label: 'Vue', dismissLabel: 'Fermer Vue' }, global })
    expect(wrapper.attributes('aria-label')).toBe('Fermer Vue')
  })
})

describe('cspTag: polymorphism', () => {
  it('static can be rendered `as`', () => {
    const wrapper = mount(CspTag, { props: { label: 'X', as: 'li' }, global })
    expect(wrapper.element.tagName).toBe('LI')
  })
})

describe('cspTagGroup: integration', () => {
  function mountGroup(groupProps: Record<string, unknown>) {
    const Host = defineComponent({
      components: { CspTag, CspTagGroup },
      props: { groupProps: { type: Object, required: true } },
      template: `
        <CspTagGroup v-bind="groupProps">
          <CspTag variant="selectable" value="a" label="A" />
          <CspTag variant="selectable" value="b" label="B" />
        </CspTagGroup>
      `,
    })
    return mount(Host, { props: { groupProps }, global })
  }

  it('a selectable inside a group becomes a ToggleGroupItem', () => {
    const wrapper = mountGroup({ modelValue: [] })
    expect(wrapper.findAll('[data-reka-collection-item]')).toHaveLength(2)
  })

  it('inherits the size enforced by the group', () => {
    const wrapper = mountGroup({ modelValue: [], size: 'sm' })
    expect(wrapper.findAll('.csp-tag--sm')).toHaveLength(2)
  })

  it('single mode: selecting an item updates the v-model', async () => {
    const onUpdate = vi.fn()
    const wrapper = mountGroup({ 'modelValue': 'a', 'type': 'single', 'onUpdate:modelValue': onUpdate })
    const buttons = wrapper.findAll('button')
    await buttons[1].trigger('click')
    expect(onUpdate).toHaveBeenCalledWith('b')
  })
})
