import { render, screen } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { setupUser } from '@/test/render'
import CandidatureNoteMessage from './CandidatureNoteMessage.vue'

function renderMessage({ scrollHeight }: { scrollHeight: number }) {
  const getComputedStyle = window.getComputedStyle
  vi.spyOn(window, 'getComputedStyle').mockImplementation(element =>
    element.tagName === 'P' ? { lineHeight: '21px' } as CSSStyleDeclaration : getComputedStyle(element),
  )
  vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(100)
  vi.spyOn(HTMLElement.prototype, 'scrollHeight', 'get').mockReturnValue(scrollHeight)
  render(CandidatureNoteMessage, { props: { message: 'Profil solide' } })
}

describe('candidatureNoteMessage', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('lets the reader unfold and fold back a note longer than five lines', async () => {
    const user = setupUser()
    renderMessage({ scrollHeight: 160 })

    await user.click(await screen.findByRole('button', { name: 'Afficher plus', expanded: false }))
    await user.click(screen.getByRole('button', { name: 'Afficher moins', expanded: true }))

    expect(screen.getByRole('button', { name: 'Afficher plus', expanded: false })).toBeInTheDocument()
  })

  it('shows a short note without toggle, despite the font overflowing its line by a few pixels', async () => {
    renderMessage({ scrollHeight: 102 })

    expect(await screen.findByText('Profil solide')).toBeInTheDocument()
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })
})
