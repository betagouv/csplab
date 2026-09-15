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

  it('opens the full list as soon as the input takes focus', async () => {
    const wrapper = mountCombobox()
    await wrapper.find('input').trigger('focus')
    await nextTick()

    expect(document.querySelectorAll('[role="option"]')).toHaveLength(OPTIONS.length)
    wrapper.unmount()
  })

  it('shows the label of the selected option in the input, not its value', async () => {
    const wrapper = mountCombobox()
    await openList(wrapper)
    document.querySelector<HTMLElement>('[role="option"]')!.click()
    await nextTick()
    await nextTick()

    expect(wrapper.find('input').element.value).toBe('Premier élément')
    expect(wrapper.emitted('update:modelValue')).toEqual([['one']])
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

  it('announces the result count in the status region after debounce', async () => {
    vi.useFakeTimers()
    const wrapper = mountCombobox()
    await openList(wrapper)
    const status = wrapper.find('[role="status"]')
    expect(status.text()).toBe('')
    await vi.advanceTimersByTimeAsync(1000)
    expect(status.text()).toBe('2 résultats')
    wrapper.unmount()
    vi.useRealTimers()
  })

  it('falls back to the empty label in the status region when no option matches', async () => {
    vi.useFakeTimers()
    const wrapper = mountCombobox({ options: [], emptyLabel: 'Aucun résultat' })
    await openList(wrapper)
    await vi.advanceTimersByTimeAsync(1000)
    expect(wrapper.find('[role="status"]').text()).toBe('Aucun résultat')
    wrapper.unmount()
    vi.useRealTimers()
  })
})
