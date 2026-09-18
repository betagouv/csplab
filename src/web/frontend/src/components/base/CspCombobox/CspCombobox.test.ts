import { render, screen } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { setupUser } from '@/test/render'
import CspCombobox from './CspCombobox.vue'

const OPTIONS = [
  { value: 'one', label: 'Premier élément', description: 'premier@exemple.fr' },
  { value: 'two', label: 'Deuxième élément', description: 'deuxieme@exemple.fr' },
]

function renderCombobox(props: Record<string, unknown> = {}) {
  const result = render(CspCombobox, {
    props: { options: OPTIONS, label: 'Rechercher un élément', ...props },
  })
  return { ...result, input: result.getByRole('combobox', { name: 'Rechercher un élément' }) }
}

async function openList(user: ReturnType<typeof setupUser>, input: HTMLElement) {
  await user.type(input, 'élément')
  await user.keyboard('{ArrowDown}')
  return screen.findByRole('listbox')
}

describe('cspCombobox', () => {
  afterEach(() => {
    vi.useRealTimers()
  })

  it('links the hint to the input', () => {
    const { input } = renderCombobox({ hint: 'Recherchez par nom' })
    expect(input).toHaveAccessibleDescription('Recherchez par nom')
  })

  it('renders options with their description when open', async () => {
    const user = setupUser()
    const { input } = renderCombobox()

    const listbox = await openList(user, input)

    expect(listbox).toHaveTextContent('Premier élément')
    expect(listbox).toHaveTextContent('premier@exemple.fr')
  })

  it('opens the full list as soon as the input takes focus', async () => {
    const user = setupUser()
    const { input } = renderCombobox()

    await user.click(input)

    expect(await screen.findAllByRole('option')).toHaveLength(OPTIONS.length)
  })

  it('shows the label of the selected option in the input, not its value', async () => {
    const user = setupUser()
    const { input, emitted } = renderCombobox()
    await openList(user, input)

    await user.click(screen.getAllByRole('option')[0]!)

    expect(input).toHaveValue('Premier élément')
    expect(emitted()['update:modelValue']).toEqual([['one']])
  })

  it('renders the action option last and emits action on select', async () => {
    const user = setupUser()
    const { input, emitted } = renderCombobox({ actionLabel: 'Créer un nouvel élément' })
    await openList(user, input)

    const action = screen.getAllByRole('option').at(-1)!
    expect(action).toHaveTextContent('Créer un nouvel élément')

    await user.click(action)

    expect(emitted().action).toHaveLength(1)
    expect(emitted()['update:modelValue']).toBeUndefined()
  })

  it('announces the result count in the status region after debounce', async () => {
    vi.useFakeTimers()
    const user = setupUser({ advanceTimers: vi.advanceTimersByTime })
    const { input, getByRole } = renderCombobox()
    await openList(user, input)

    expect(getByRole('status').textContent).toBe('')

    await vi.advanceTimersByTimeAsync(1000)

    expect(getByRole('status')).toHaveTextContent('2 résultats')
  })

  it('falls back to the empty label in the status region when no option matches', async () => {
    vi.useFakeTimers()
    const user = setupUser({ advanceTimers: vi.advanceTimersByTime })
    const { input, getByRole } = renderCombobox({ options: [], emptyLabel: 'Aucun résultat' })
    await user.type(input, 'élément')

    await vi.advanceTimersByTimeAsync(1000)

    expect(getByRole('status')).toHaveTextContent('Aucun résultat')
  })
})
