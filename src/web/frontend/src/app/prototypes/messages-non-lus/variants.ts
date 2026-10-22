import type { InjectionKey, Ref } from 'vue'

export const UNREAD_VARIANTS = [
  { id: 'maquette', name: 'Ligne de la maquette' },
  { id: 'maquette-icone', name: 'Ligne de la maquette, avec une icône' },
  { id: 'point-nom', name: 'Point à côté du nom' },
  { id: 'compteur-nom', name: 'Compteur à côté du nom' },
  { id: 'icone-date', name: 'Icône sur la ligne de la date' },
  { id: 'badge-statut', name: 'Badge de statut' },
  { id: 'pied-lien', name: 'Pied de carte vers les messages' },
] as const

export type UnreadVariant = typeof UNREAD_VARIANTS[number]['id']

export const DEFAULT_UNREAD_VARIANT: UnreadVariant = 'maquette'

export const UNREAD_VARIANT_KEY: InjectionKey<Ref<UnreadVariant>> = Symbol('unread-variant')

export const UNREAD_COLORS = [
  { id: 'bleu', name: 'Bleu' },
  { id: 'rouge', name: 'Rouge' },
] as const

export type UnreadColor = typeof UNREAD_COLORS[number]['id']

export const DEFAULT_UNREAD_COLOR: UnreadColor = 'bleu'

export function applyUnreadColor(root: HTMLElement, color: UnreadColor): void {
  root.setAttribute('data-csp-unread-color', color)
}
