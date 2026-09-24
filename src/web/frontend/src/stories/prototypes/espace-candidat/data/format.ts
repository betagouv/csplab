// Date « maintenant » figée pour que le prototype reste déterministe (tri, « aujourd'hui », « hier »).
export const MAINTENANT_REFERENCE = new Date(2026, 8, 24, 10, 30)

const MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

function memeJour(a: Date, b: Date): boolean {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
}

function veille(d: Date): Date {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate() - 1)
}

export function formaterDateLongue(d: Date): string {
  return `${d.getDate()} ${MOIS[d.getMonth()]} ${d.getFullYear()}`
}

export function formaterDateCourte(d: Date): string {
  return `${d.getDate()} ${MOIS[d.getMonth()]}`
}

export function formaterHeure(d: Date): string {
  return `${d.getHours()}h${String(d.getMinutes()).padStart(2, '0')}`
}

// « aujourd'hui » / « hier » / « 12 septembre » — pour la dernière activité d'une candidature.
export function formaterActivite(d: Date, maintenant = MAINTENANT_REFERENCE): string {
  if (memeJour(d, maintenant)) {
    return 'aujourd\'hui'
  }
  if (memeJour(d, veille(maintenant))) {
    return 'hier'
  }
  return formaterDateCourte(d)
}

// « Aujourd'hui, 9h05 » / « Hier, 14h20 » / « 12 septembre, 9h05 » — pour l'horodatage d'un message.
export function formaterDateHeure(d: Date, maintenant = MAINTENANT_REFERENCE): string {
  if (memeJour(d, maintenant)) {
    return `Aujourd'hui, ${formaterHeure(d)}`
  }
  if (memeJour(d, veille(maintenant))) {
    return `Hier, ${formaterHeure(d)}`
  }
  return `${formaterDateCourte(d)}, ${formaterHeure(d)}`
}
