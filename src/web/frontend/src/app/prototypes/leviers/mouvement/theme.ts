import type { Animation, Passage, PisteMouvement } from './pistes'

// The motion rule of the interface theme applied to the page, read from the motion roles of csp-variables.css as the
// theme sets them, reduced motion included: the timeline of a theme then has no values of its own
function lire(nom: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(nom).trim()
}

// One animation of the shorthand « keyframes duration timing-function »; none, or a role left to the components, plays
// nothing
function animation(valeur: string): Animation | null {
  const [keyframes, duree, ...courbe] = valeur.split(' ')
  return keyframes && duree?.endsWith('ms') ? { keyframes, duree: Number.parseInt(duree, 10), courbe: courbe.join(' ') } : null
}

function passage(role: string): Passage {
  return { entree: animation(lire(`--csp-motion-${role}-enter`)), sortie: animation(lire(`--csp-motion-${role}-exit`)) }
}

export function regleDuTheme(id: string, nom: string): PisteMouvement {
  return {
    id,
    nom,
    etat: Number.parseInt(lire('--csp-motion-duration-state'), 10) || 0,
    couche: passage('overlap'),
    dialogue: passage('dialog'),
    tiroir: passage('drawer'),
    voile: passage('scrim'),
    depot: lire('--csp-motion-raised-drop').split(/,(?![^(]*\))/).flatMap(valeur => animation(valeur.trim()) ?? []),
  }
}
