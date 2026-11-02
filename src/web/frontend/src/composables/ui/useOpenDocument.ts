import type { ToastOptions } from './useToast'
import { isHttpStatus } from '@/api/errors'
import { useToast } from './useToast'

const BLOCKED_TOAST: ToastOptions = {
  variant: 'error',
  title: 'Le navigateur a bloqué l\'ouverture du document',
  description: 'Autorisez les fenêtres pop-up pour ce site, puis réessayez.',
}

function failureToast(error: unknown): ToastOptions {
  if (isHttpStatus(error, 404)) {
    return { variant: 'error', title: 'Le document est introuvable' }
  }
  if (isHttpStatus(error, 415)) {
    return { variant: 'error', title: 'Ce format de document ne peut pas être affiché' }
  }
  return { variant: 'error', title: 'L\'ouverture du document a échoué', description: 'Réessayez dans quelques instants.' }
}

export function useOpenDocument() {
  const { addToast } = useToast()

  async function open(event: MouseEvent, url: string, check: () => Promise<void>): Promise<void> {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return
    }
    event.preventDefault()
    const tab = window.open('', '_blank')
    try {
      await check()
    }
    catch (error) {
      tab?.close()
      addToast(failureToast(error))
      return
    }
    if (!tab) {
      addToast(BLOCKED_TOAST)
      return
    }
    tab.opener = null
    tab.location.href = url
  }

  return { open }
}
