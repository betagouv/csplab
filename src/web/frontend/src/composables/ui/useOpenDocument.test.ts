import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError, NetworkError } from '@/api/errors'
import { useOpenDocument } from './useOpenDocument'
import { useToast } from './useToast'

const URL = '/documents/1'

function mockTab() {
  const tab = { opener: window as Window | null, location: { href: '' }, close: vi.fn() }
  vi.spyOn(window, 'open').mockReturnValue(tab as unknown as Window)
  return tab
}

function lastToast() {
  const { toasts, dismissToast } = useToast()
  const toast = toasts.value.at(-1)!
  dismissToast(toast.id)
  return toast
}

describe('useOpenDocument', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows the document in the tab opened by the click', async () => {
    const tab = mockTab()
    const event = new MouseEvent('click', { cancelable: true })

    await useOpenDocument().open(event, URL, async () => {})

    expect(event.defaultPrevented).toBe(true)
    expect(tab.location.href).toBe(URL)
    expect(tab.opener).toBeNull()
  })

  it.each([
    [new HttpError(404, 'Not Found'), 'Le document est introuvable'],
    [new HttpError(415, 'Unsupported Media Type'), 'Ce format de document ne peut pas être affiché'],
    [new NetworkError(new TypeError('Failed to fetch')), 'L\'ouverture du document a échoué'],
  ])('closes the tab and explains the failure (%s)', async (error, title) => {
    const tab = mockTab()

    await useOpenDocument().open(new MouseEvent('click'), URL, async () => {
      throw error
    })

    expect(tab.close).toHaveBeenCalled()
    expect(lastToast()).toMatchObject({ variant: 'error', title })
  })

  it('explains when the browser blocks the new tab', async () => {
    vi.spyOn(window, 'open').mockReturnValue(null)

    await useOpenDocument().open(new MouseEvent('click'), URL, async () => {})

    expect(lastToast()).toMatchObject({ variant: 'error', title: 'Le navigateur a bloqué l\'ouverture du document' })
  })

  it('lets the browser handle a click with a modifier key', async () => {
    const open = vi.spyOn(window, 'open')
    const check = vi.fn()
    const event = new MouseEvent('click', { cancelable: true, metaKey: true })

    await useOpenDocument().open(event, URL, check)

    expect(event.defaultPrevented).toBe(false)
    expect(open).not.toHaveBeenCalled()
    expect(check).not.toHaveBeenCalled()
  })
})
