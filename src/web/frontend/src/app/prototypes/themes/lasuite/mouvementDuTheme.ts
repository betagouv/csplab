import type { Animation, Passage, PisteMouvement } from '../../leviers/mouvement/pistes'

// Animations of a motion role as the root element computes it, such as « csp-drawer-enter 250ms cubic-bezier(…) »
function animations(valeur: string): Animation[] {
  return valeur
    .split(/,(?![^(]*\))/)
    .map(partie => partie.trim().split(/\s+/))
    .filter(([, duree]) => duree?.endsWith('ms'))
    .map(([keyframes, duree, ...courbe]) => ({ keyframes: keyframes!, duree: Number.parseInt(duree!), courbe: courbe.join(' ') }))
}

function lire(style: CSSStyleDeclaration, role: string): Animation | null {
  return animations(style.getPropertyValue(`--csp-motion-${role}`))[0] ?? null
}

function passage(style: CSSStyleDeclaration, role: string): Passage {
  return { entree: lire(style, `${role}-enter`), sortie: lire(style, `${role}-exit`) }
}

// The motion of the theme applied to the page, read from its variables, for the timeline of a plate
export function mouvementDuTheme(id: string, nom: string): PisteMouvement {
  const style = getComputedStyle(document.documentElement)
  return {
    id,
    nom,
    etat: Number.parseInt(style.getPropertyValue('--csp-motion-duration-state')) || 0,
    couche: passage(style, 'overlap'),
    dialogue: passage(style, 'dialog'),
    tiroir: passage(style, 'drawer'),
    voile: passage(style, 'scrim'),
    depot: animations(style.getPropertyValue('--csp-motion-raised-drop')),
  }
}
