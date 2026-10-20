import type { LevierOption, Valeurs } from '../options'

// One animation of a motion role: keyframes of styles/themes/motion.css, duration in ms, timing function
export interface Animation {
  keyframes: string
  duree: number
  courbe: string
}

// Entrance and exit of a layer; null leaves it instant
export interface Passage {
  entree: Animation | null
  sortie: Animation | null
}

export interface PisteMouvement {
  id: string
  nom: string
  // Duration of the colour changes of buttons, sidebar items and kanban cards, with the ease curve of CSS transitions
  etat: number
  couche: Passage
  dialogue: Passage
  tiroir: Passage
  voile: Passage
  // Animations played together by a card dropped in another column
  depot: Animation[]
  // Entrance of the tooltip, when it keeps a fade of its own while the other layers appear at once
  bulle?: Animation
}

export type Role = 'etat' | 'couche' | 'dialogue' | 'voile' | 'tiroir' | 'depot'

export const ROLES: Record<Role, string> = {
  etat: 'Changement d’état',
  couche: 'Menu, liste de choix, bulle',
  dialogue: 'Dialogue',
  voile: 'Voile',
  tiroir: 'Panneau',
  depot: 'Carte déposée',
}

// What each keyframes does, as the timeline names it
export const NATURE: Record<string, string> = {
  'csp-fade-in': 'fondu',
  'csp-fade-out': 'fondu',
  'csp-overlap-enter': 'descend de 4 px en fondu',
  'csp-overlap-unfold': 'se déplie depuis son bouton',
  'csp-dialog-enter': 'grandit de 2 % en fondu',
  'csp-dialog-rise': 'monte de 24 px en fondu',
  'csp-dialog-exit': 'rétrécit de 2 % en fondu',
  'csp-drawer-enter': 'glisse depuis le bord',
  'csp-drawer-exit': 'glisse vers le bord',
  'csp-raised-drop': 'fond gris qui s’efface',
  'csp-raised-outline-drop': 'contour bleu qui s’efface',
  'csp-raised-settle': 'glisse jusqu’à sa place',
}

function animation(keyframes: string, duree: number, courbe: string): Animation {
  return { keyframes, duree, courbe }
}

// An element that arrives slows down at its place; an element that leaves speeds up
const ARRIVEE = 'cubic-bezier(0, 0, 0.38, 0.9)'
const DEPART = 'cubic-bezier(0.2, 0, 1, 0.9)'
const ARRIVEE_MARQUEE = 'cubic-bezier(0.05, 0.7, 0.1, 1)'
const DEPART_MARQUE = 'cubic-bezier(0.3, 0, 0.8, 0.15)'

const IMMOBILE: Passage = { entree: null, sortie: null }

// Everything changes at once, but the tooltip, which fades in with the fallback of CspTooltip
export const KIT: PisteMouvement = {
  id: 'kit',
  nom: 'Aujourd’hui',
  etat: 0,
  couche: IMMOBILE,
  dialogue: IMMOBILE,
  tiroir: IMMOBILE,
  voile: IMMOBILE,
  depot: [],
  bulle: animation('csp-fade-in', 120, 'ease-out'),
}

const FONDU_DSFR: Passage = { entree: animation('csp-fade-in', 300, 'ease'), sortie: animation('csp-fade-out', 300, 'ease') }

// The single duration of the DSFR, with its ease curve, on everything that appears; colour changes stay instant
export const DUREE_DSFR: PisteMouvement = {
  id: 'dsfr',
  nom: '300 ms du DSFR',
  etat: 0,
  couche: FONDU_DSFR,
  dialogue: FONDU_DSFR,
  tiroir: { entree: animation('csp-drawer-enter', 300, 'ease'), sortie: animation('csp-drawer-exit', 300, 'ease') },
  voile: FONDU_DSFR,
  depot: [animation('csp-raised-outline-drop', 300, 'ease')],
}

// A duration that grows with the surface that moves, an exit shorter than the entrance
export const DUREES_PAR_ROLE: PisteMouvement = {
  id: 'roles',
  nom: 'Durées par rôle',
  etat: 100,
  couche: { entree: animation('csp-fade-in', 150, ARRIVEE), sortie: animation('csp-fade-out', 100, DEPART) },
  dialogue: { entree: animation('csp-dialog-enter', 200, ARRIVEE), sortie: animation('csp-dialog-exit', 150, DEPART) },
  tiroir: { entree: animation('csp-drawer-enter', 300, ARRIVEE), sortie: animation('csp-drawer-exit', 200, DEPART) },
  voile: { entree: animation('csp-fade-in', 200, ARRIVEE), sortie: animation('csp-fade-out', 150, DEPART) },
  depot: [animation('csp-raised-drop', 700, DEPART)],
}

// Each element comes from what makes it appear: the menu from its button, the card from the point where it was released
export const TRAJECTOIRES: PisteMouvement = {
  id: 'trajectoires',
  nom: 'Trajectoires',
  etat: 150,
  couche: { entree: animation('csp-overlap-unfold', 200, ARRIVEE_MARQUEE), sortie: animation('csp-fade-out', 150, DEPART_MARQUE) },
  dialogue: { entree: animation('csp-dialog-rise', 300, ARRIVEE_MARQUEE), sortie: animation('csp-dialog-exit', 150, DEPART_MARQUE) },
  tiroir: { entree: animation('csp-drawer-enter', 450, ARRIVEE_MARQUEE), sortie: animation('csp-drawer-exit', 250, DEPART_MARQUE) },
  voile: { entree: animation('csp-fade-in', 300, ARRIVEE), sortie: animation('csp-fade-out', 250, DEPART) },
  depot: [animation('csp-raised-settle', 350, ARRIVEE_MARQUEE), animation('csp-raised-drop', 900, DEPART)],
}

export const PISTES: PisteMouvement[] = [KIT, DUREE_DSFR, DUREES_PAR_ROLE, TRAJECTOIRES]

// Under reduced motion nothing moves nor scales: layers fade, in 200 ms at most so that two layers do not show through
// each other for long, and colour changes stay
const FONDU: Record<string, string | null> = {
  'csp-fade-in': 'csp-fade-in',
  'csp-fade-out': 'csp-fade-out',
  'csp-overlap-enter': 'csp-fade-in',
  'csp-overlap-unfold': 'csp-fade-in',
  'csp-dialog-enter': 'csp-fade-in',
  'csp-dialog-rise': 'csp-fade-in',
  'csp-dialog-exit': 'csp-fade-out',
  'csp-drawer-enter': 'csp-fade-in',
  'csp-drawer-exit': 'csp-fade-out',
  'csp-raised-settle': null,
}

const FONDU_MAX = 200

function sansDeplacement(anim: Animation | null): Animation | null {
  if (!anim || !(anim.keyframes in FONDU)) {
    return anim
  }
  const keyframes = FONDU[anim.keyframes]
  return keyframes ? { ...anim, keyframes, duree: Math.min(anim.duree, FONDU_MAX) } : null
}

function passageReduit({ entree, sortie }: Passage): Passage {
  return { entree: sansDeplacement(entree), sortie: sansDeplacement(sortie) }
}

export function reduite(piste: PisteMouvement): PisteMouvement {
  return {
    ...piste,
    couche: passageReduit(piste.couche),
    dialogue: passageReduit(piste.dialogue),
    tiroir: passageReduit(piste.tiroir),
    voile: passageReduit(piste.voile),
    depot: piste.depot.flatMap(anim => sansDeplacement(anim) ?? []),
  }
}

function css(anim: Animation | null): string {
  return anim ? `${anim.keyframes} ${anim.duree}ms ${anim.courbe}` : 'none'
}

function valeurs(piste: PisteMouvement): Valeurs {
  return {
    '--csp-motion-duration-state': `${piste.etat}ms`,
    '--csp-motion-overlap-enter': css(piste.couche.entree),
    '--csp-motion-overlap-exit': css(piste.couche.sortie),
    '--csp-motion-dialog-enter': css(piste.dialogue.entree),
    '--csp-motion-dialog-exit': css(piste.dialogue.sortie),
    '--csp-motion-drawer-enter': css(piste.tiroir.entree),
    '--csp-motion-drawer-exit': css(piste.tiroir.sortie),
    '--csp-motion-scrim-enter': css(piste.voile.entree),
    '--csp-motion-scrim-exit': css(piste.voile.sortie),
    '--csp-motion-raised-drop': piste.depot.length ? piste.depot.map(css).join(', ') : 'none',
  }
}

// The kit option writes nothing, so that the tooltip keeps its own fade
export const MOUVEMENT: LevierOption[] = PISTES.map(piste => piste === KIT
  ? { id: piste.id, nom: piste.nom, valeurs: {} }
  : { id: piste.id, nom: piste.nom, valeurs: valeurs(piste), reduit: valeurs(reduite(piste)) })
