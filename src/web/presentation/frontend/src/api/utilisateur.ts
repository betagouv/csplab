import type { components } from '@/types/api'
import { api } from '@/utils/api'

export type Utilisateur = components['schemas']['Utilisateur']

export async function getMe(): Promise<Utilisateur> {
  const { data } = await api.GET('/utilisateur/me')
  return data!
}
