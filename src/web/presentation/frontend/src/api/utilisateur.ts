import type { components } from '@/types/api'
import { api } from '@/api/client'

export type Utilisateur = components['schemas']['Utilisateur']

export async function getMe(): Promise<Utilisateur> {
  const { data } = await api.GET('/utilisateur/me')
  return data!
}
