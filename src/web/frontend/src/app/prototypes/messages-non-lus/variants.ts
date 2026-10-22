import type { InjectionKey, Ref } from 'vue'

export const UNREAD_VARIANTS = [
  { id: 'maquette', name: 'Ligne de la maquette' },
  { id: 'point-nom', name: 'Point à côté du nom' },
  { id: 'compteur-nom', name: 'Compteur à côté du nom' },
  { id: 'icone-date', name: 'Icône sur la ligne de la date' },
  { id: 'badge-statut', name: 'Badge de statut' },
  { id: 'pied-lien', name: 'Pied de carte vers les messages' },
] as const

export type UnreadVariant = typeof UNREAD_VARIANTS[number]['id']

export const DEFAULT_UNREAD_VARIANT: UnreadVariant = 'maquette'

export const UNREAD_VARIANT_KEY: InjectionKey<Ref<UnreadVariant>> = Symbol('unread-variant')
