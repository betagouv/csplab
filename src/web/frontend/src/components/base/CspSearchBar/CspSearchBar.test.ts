import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { setupUser } from '@/test/render'
import CspSearchBar from './CspSearchBar.vue'

function renderBar(props: Record<string, unknown> = {}) {
  return render(CspSearchBar, { props: { label: 'Rechercher un élément', ...props } })
}

describe('cspSearchBar', () => {
  it('launches the search with the trimmed value from the button and from the Enter key', async () => {
    const user = setupUser()
    const { emitted } = renderBar()

    await user.type(screen.getByRole('searchbox', { name: 'Rechercher un élément' }), '  foo {Enter}')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toEqual([['foo'], ['foo']])
  })

  it('keeps the Enter key from submitting an enclosing form', async () => {
    const user = setupUser()
    let submitted = false
    const form = document.createElement('form')
    form.addEventListener('submit', (event) => {
      event.preventDefault()
      submitted = true
    })
    document.body.appendChild(form)
    render(CspSearchBar, { props: { label: 'Rechercher un élément' }, container: form })

    await user.type(screen.getByRole('searchbox'), 'foo{Enter}')

    expect(submitted).toBe(false)
    form.remove()
  })

  it('replaces the button with a decorative icon when the search follows the typing', async () => {
    const user = setupUser()
    const { emitted } = renderBar({ mode: 'live' })

    expect(screen.queryByRole('button')).not.toBeInTheDocument()
    await user.type(screen.getByRole('searchbox', { name: 'Rechercher un élément' }), 'foo{Enter}')

    expect(emitted()['update:modelValue']).toContainEqual(['foo'])
    expect(emitted().search).toEqual([['foo']])
  })

  it('launches nothing while disabled', async () => {
    const user = setupUser()
    const { emitted } = renderBar({ disabled: true, modelValue: 'foo' })

    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toBeUndefined()
  })

  it('describes the field with its error message', () => {
    renderBar({ error: true, errorMessage: 'Aucun résultat.' })

    const field = screen.getByRole('searchbox')
    expect(field).toHaveAccessibleDescription('Aucun résultat.')
    expect(field).toBeInvalid()
  })
})
