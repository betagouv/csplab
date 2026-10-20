const NOMMEES: Record<string, [number, number, number, number]> = {
  'linear': [0, 0, 1, 1],
  'ease': [0.25, 0.1, 0.25, 1],
  'ease-in': [0.42, 0, 1, 1],
  'ease-out': [0, 0, 0.58, 1],
  'ease-in-out': [0.42, 0, 0.58, 1],
}

function points(courbe: string): [number, number, number, number] {
  const nommee = NOMMEES[courbe]
  if (nommee) {
    return nommee
  }
  const valeurs = courbe.match(/-?[\d.]+/g)?.map(Number) ?? []
  return valeurs.length === 4 ? valeurs as [number, number, number, number] : NOMMEES.linear!
}

function bezier(s: number, a: number, b: number): number {
  return 3 * a * s * (1 - s) ** 2 + 3 * b * s ** 2 * (1 - s) + s ** 3
}

// Progress of a CSS timing function at the share t of its duration, between 0 and 1
export function progression(courbe: string, t: number): number {
  const [x1, y1, x2, y2] = points(courbe)
  let bas = 0
  let haut = 1
  for (let pas = 0; pas < 30; pas++) {
    const milieu = (bas + haut) / 2
    if (bezier(milieu, x1, x2) < t) {
      bas = milieu
    }
    else {
      haut = milieu
    }
  }
  return bezier((bas + haut) / 2, y1, y2)
}
