import type { components } from '@/types/api'
import { api, readCsrfCookie } from '@/api/client'
import { can } from '@/utils/authorizedActions'

export type Utilisateur = components['schemas']['Utilisateur']

export type UserOrganisme = Utilisateur['organismes'][number]

export function canBrowseOrganismes(user: Utilisateur | null | undefined): boolean {
  return can(user?.authorized_actions, 'list_organismes')
}

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
