import { mount } from '@vue/test-utils'
import { beforeAll, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import CspCombobox from './CspCombobox.vue'

beforeAll(() => {
  Element.prototype.scrollIntoView = vi.fn()
})

const OPTIONS = [
  { value: 'one', label: 'Premier élément', description: 'premier@exemple.fr' },
  { value: 'two', label: 'Deuxième élément', description: 'deuxieme@exemple.fr' },
]

function mountCombobox(props: Record<string, unknown> = {}) {
  return mount(CspCombobox, {
    props: {
      options: OPTIONS,
      label: 'Rechercher un élément',
      ...props,
    },
    attachTo: document.body,
  })
}

async function openList(wrapper: ReturnType<typeof mountCombobox>) {
  const input = wrapper.find('input')
  await input.setValue('élément')
  await input.trigger('keydown', { key: 'ArrowDown' })
  await nextTick()
}

describe('cspCombobox', () => {
  it('exposes the aria combobox pattern on the input', () => {
    const wrapper = mountCombobox()
    const input = wrapper.find('input')
    expect(input.attributes('role')).toBe('combobox')
    expect(input.attributes('aria-expanded')).toBe('false')
    expect(input.attributes('aria-autocomplete')).toBe('list')
    wrapper.unmount()
  })

  it('links the hint to the input', () => {
    const wrapper = mountCombobox({ hint: 'Recherchez par nom' })
    const input = wrapper.find('input')
    const hintId = input.attributes('aria-describedby')
    expect(hintId).toBeTruthy()
    expect(document.getElementById(hintId!)?.textContent).toContain('Recherchez par nom')
    wrapper.unmount()
  })

  it('renders options with their description when open', async () => {
    const wrapper = mountCombobox()
    await openList(wrapper)
    const listbox = document.querySelector('[role="listbox"]')
    expect(listbox).toBeTruthy()
    expect(listbox!.textContent).toContain('Premier élément')
    expect(listbox!.textContent).toContain('premier@exemple.fr')
    wrapper.unmount()
  })

  it('renders the action option last and emits action on select', async () => {
    const wrapper = mountCombobox({ actionLabel: 'Créer un nouvel élément' })
    await openList(wrapper)
    const options = [...document.querySelectorAll('[role="option"]')]
    expect(options.at(-1)?.textContent).toContain('Créer un nouvel élément')

    ;(options.at(-1) as HTMLElement).click()
    await nextTick()
    expect(wrapper.emitted('action')).toHaveLength(1)
    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
    wrapper.unmount()
  })

  it('exposes a status region', () => {
    const wrapper = mountCombobox()
    expect(wrapper.find('[role="status"]').exists()).toBe(true)
    wrapper.unmount()
  })
})
