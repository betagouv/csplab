import type { components } from '@/types/api'
import { api, readCsrfCookie } from '@/api/client'

export type Utilisateur = components['schemas']['Utilisateur']

export async function getMe(): Promise<Utilisateur> {
  const { data } = await api.GET('/utilisateur/me')
  return data!
}

export function logout(): void {
  const form = document.createElement('form')
  form.method = 'POST'
  form.action = '/utilisateur/deconnexion'
  form.hidden = true

  const csrfToken = document.createElement('input')
  csrfToken.type = 'hidden'
  csrfToken.name = 'csrfmiddlewaretoken'
  csrfToken.value = readCsrfCookie()
  form.append(csrfToken)

  document.body.append(form)
  form.submit()
}
