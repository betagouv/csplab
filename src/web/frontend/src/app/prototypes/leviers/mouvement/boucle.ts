// Loops of the motion demos. Every frame derives its position in the loop from the clock of the computer and from a
// common origin, so the screens of a comparison, each in its own frame, and the timeline that runs below them play the
// same moment. A screen of a plate tells the plate when its application is ready; once all its screens are, the plate
// sends them the origin.

export type Geste = 'menu' | 'panneau' | 'depot' | 'dialogue'
export type Demo = Geste | 'parcours'

// entree: a layer or a card appears; sortie: a layer goes
export type Sens = 'entree' | 'sortie'

export type Action = 'viser' | 'ouvrir' | 'fermer' | 'saisir' | 'deposer'

export interface Etape {
  at: number
  geste: Geste
  action: Action
  // Moment that the timeline follows from this step
  sens?: Sens
}

export interface Boucle {
  duree: number
  // Time that the timeline gives to an animation, which the slow motion stretches
  fenetre: number
  etapes: Etape[]
  // Start of each gesture in the loop
  debuts: { at: number, geste: Geste }[]
}

export const PARCOURS: Geste[] = ['menu', 'panneau', 'depot', 'dialogue']

// The pointer reaches its target before the click
const VISEE = 400
// Time the pointer takes to carry a card to another column
export const GLISSER = 1200

function etapesDe(geste: Geste, fenetre: number): { duree: number, etapes: Omit<Etape, 'geste'>[] } {
  switch (geste) {
    case 'menu': {
      const fermeture = 800 + fenetre + 1100
      return {
        duree: fermeture + fenetre + 500,
        etapes: [
          { at: 800 - VISEE, action: 'viser' },
          { at: 800, action: 'ouvrir', sens: 'entree' },
          { at: fermeture - VISEE, action: 'viser' },
          { at: fermeture, action: 'fermer', sens: 'sortie' },
        ],
      }
    }
    case 'panneau': {
      const fermeture = 800 + fenetre + 1700
      return {
        duree: fermeture + fenetre + 500,
        etapes: [
          { at: 800 - VISEE, action: 'viser' },
          { at: 800, action: 'ouvrir', sens: 'entree' },
          { at: fermeture - VISEE, action: 'viser' },
          { at: fermeture, action: 'fermer', sens: 'sortie' },
        ],
      }
    }
    case 'depot': {
      const depot = 800 + GLISSER
      return {
        duree: depot + fenetre + 800,
        etapes: [
          { at: 800 - VISEE, action: 'viser' },
          { at: 800, action: 'saisir' },
          { at: depot, action: 'deposer', sens: 'entree' },
        ],
      }
    }
    case 'dialogue': {
      const fermeture = 600 + fenetre + 1200
      return {
        duree: fermeture + fenetre + 500,
        etapes: [
          { at: 600, action: 'ouvrir', sens: 'entree' },
          { at: fermeture - VISEE, action: 'viser' },
          { at: fermeture, action: 'fermer', sens: 'sortie' },
        ],
      }
    }
  }
}

// ralenti: factor that slows the animations down, 1 at real speed
export function boucle(demo: Demo, ralenti = 1): Boucle {
  const fenetre = 1000 * ralenti
  const gestes = demo === 'parcours' ? PARCOURS : [demo]
  let debut = 0
  const etapes: Etape[] = []
  const debuts: Boucle['debuts'] = []
  for (const geste of gestes) {
    const { duree, etapes: steps } = etapesDe(geste, fenetre)
    debuts.push({ at: debut, geste })
    etapes.push(...steps.map(step => ({ ...step, at: debut + step.at, geste })))
    debut += duree
  }
  return { duree: debut, fenetre, etapes, debuts }
}

export const MESSAGE_PRET = 'mouvement-pret'
export const MESSAGE_ORIGINE = 'mouvement-origine'

// Time in the loop that started at origine, a time of the clock
export function instant(loop: Boucle, origine: number): number {
  return (Date.now() - origine) % loop.duree
}

// Gesture and moment that the timeline follows at time t of the loop, with the time spent in the animation
export function momentA(loop: Boucle, t: number, ralenti = 1): { geste: Geste, sens: Sens, ecoule: number } | null {
  for (const etape of loop.etapes) {
    if (etape.sens && t >= etape.at && t < etape.at + loop.fenetre) {
      return { geste: etape.geste, sens: etape.sens, ecoule: (t - etape.at) / ralenti }
    }
  }
  return null
}
