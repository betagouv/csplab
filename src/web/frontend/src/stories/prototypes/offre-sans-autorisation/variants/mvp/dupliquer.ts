// Dupliquer une offre (retour PO, L9) : ouvre directement le formulaire pré-rempli, sans écran intermédiaire.

import type { Nav } from './nav'
import type { Offre } from './store'
import { nouvelleOffre } from './store'

export function dupliquer(source: Offre, { aller, notifier }: Pick<Nav, 'aller' | 'notifier'>) {
  const o = nouvelleOffre(undefined, 'duplication', source)
  notifier(`Copie de « ${source.titre || source.id} » créée (${o.id}). Nombre de postes et dates vidés.`)
  aller({ nom: 'rediger', id: o.id })
}
