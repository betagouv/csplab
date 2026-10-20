import type { Geste, Sens } from './boucle'
import type { Animation, Passage, PisteMouvement, Role } from './pistes'
import { NATURE, ROLES } from './pistes'

// One bar of the timeline; a duration of 0 draws an instant change
export interface Barre {
  duree: number
  courbe: string
  legende: string
  // An animation that the demo does not play, such as the tooltip: the timeline runs past it
  horsDemo?: boolean
}

export interface Ligne {
  id: string
  libelle: string
  entree: Barre[]
  sortie: Barre[]
  // Gestures of the demo during which the timeline runs on this line
  gestes: Geste[]
}

// Gestures that show each role
const GESTES_DU_ROLE: Record<Role, Geste[]> = {
  etat: ['panneau'],
  couche: ['menu'],
  dialogue: ['dialogue'],
  voile: ['dialogue'],
  tiroir: ['panneau'],
  depot: ['depot'],
}

const ROLES_DU_GESTE: Record<Geste, Role[]> = {
  menu: ['couche'],
  panneau: ['tiroir'],
  dialogue: ['dialogue'],
  depot: ['depot'],
}

function barre(animation: Animation | null, prefixe: string): Barre {
  if (!animation) {
    return { duree: 0, courbe: 'linear', legende: `${prefixe}instantané` }
  }
  return {
    duree: animation.duree,
    courbe: animation.courbe,
    legende: `${prefixe}${animation.duree} ms, ${NATURE[animation.keyframes] ?? animation.keyframes}`,
  }
}

function passage(piste: PisteMouvement, role: Role): Passage | null {
  return role === 'etat' || role === 'depot' ? null : piste[role]
}

function barres(piste: PisteMouvement, role: Role, sens: Sens, prefixe: string): Barre[] {
  if (role === 'etat') {
    const duree = piste.etat
    return [{ duree, courbe: 'ease', legende: duree ? `${prefixe}${duree} ms, couleur de la carte ouverte` : `${prefixe}instantané` }]
  }
  if (role === 'depot') {
    if (sens === 'sortie') {
      return []
    }
    return piste.depot.length ? piste.depot.map(animation => barre(animation, prefixe)) : [barre(null, prefixe)]
  }
  return [barre(passage(piste, role)![sens === 'entree' ? 'entree' : 'sortie'], prefixe)]
}

// The layers of a track, with the tooltip apart when it has a fade of its own
function barresDesCouches(piste: PisteMouvement, sens: Sens): Barre[] {
  if (!piste.bulle || sens === 'sortie') {
    return barres(piste, 'couche', sens, '')
  }
  return [barre(piste.couche.entree, 'menu et liste de choix, '), { ...barre(piste.bulle, 'bulle, '), horsDemo: true }]
}

// The rule of a track: one line per role
export function lignesDuRole(piste: PisteMouvement): Ligne[] {
  return (Object.keys(ROLES) as Role[]).map(role => ({
    id: role,
    libelle: ROLES[role],
    entree: role === 'couche' ? barresDesCouches(piste, 'entree') : barres(piste, role, 'entree', ''),
    sortie: role === 'couche' ? barresDesCouches(piste, 'sortie') : barres(piste, role, 'sortie', ''),
    gestes: GESTES_DU_ROLE[role],
  }))
}

// One gesture across tracks: one line per track, one bar per role of the gesture
export function lignesDuGeste(pistes: PisteMouvement[], geste: Geste): Ligne[] {
  const roles = ROLES_DU_GESTE[geste]
  const prefixe = (role: Role) => roles.length > 1 ? `${ROLES[role]}, ` : ''
  return pistes.map(piste => ({
    id: piste.id,
    libelle: piste.nom,
    entree: roles.flatMap(role => barres(piste, role, 'entree', prefixe(role))),
    sortie: roles.flatMap(role => barres(piste, role, 'sortie', prefixe(role))),
    gestes: [geste],
  }))
}
