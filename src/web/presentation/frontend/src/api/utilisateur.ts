import type { components } from '@/types/api'
import { api, readCsrfCookie } from '@/api/client'

export type Utilisateur = components['schemas']['Utilisateur']

export async function getMe(): Promise<Utilisateur> {
  const { data } = await api.GET('/utilisateur/me')
  return data!
}

export async function logout(): Promise<void> {
  await fetch('/utilisateur/deconnexion', {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': readCsrfCookie(),
    },
  })
  window.location.href = '/'
}
