import type { components } from '@/types/api'
import { http } from '@/utils/http'

export type Utilisateur = components['schemas']['Utilisateur']

export function getMe(): Promise<Utilisateur> {
  return http.get('/utilisateur/me')
}
