// Dossiers de la session du prototype : simule le serveur. Rangés dans sessionStorage pour survivre
// à un rechargement de page (l'irritant « rafraîchissement toutes les 5 minutes » des outils actuels).

import type { OffreState } from './types'
import { reactive } from 'vue'
import { clone, etatDarBrouillon, etatDarPaie, etatDarRh, etatInitial, etatPreset, etatSansDar } from './scenario'

const CLE = 'csplab-proto-creation-offre-dossiers-v5'
const CLE_COLONNES = 'csplab-proto-creation-offre-colonnes-v5'

function lire<T>(cle: string): T | null {
  try {
    const brut = sessionStorage.getItem(cle)
    return brut ? JSON.parse(brut) as T : null
  }
  catch {
    return null
  }
}

function ecrire(cle: string, valeur: unknown) {
  try {
    sessionStorage.setItem(cle, JSON.stringify(valeur))
  }
  catch {
    // Stockage indisponible (navigation privée…) : le prototype reste utilisable, sans persistance.
  }
}

function offreExistante(reference: string, intitule: string, code: string, statut: 'creee' | 'publiee', le: string, dar: string): OffreState {
  const s = etatPreset('pret')
  s.besoin.darRef = dar
  s.organisation = 'dar_csp'
  s.circuit = []
  s.reference = reference
  s.statut = statut
  s.besoin.intitule = intitule
  s.titreAnnonce = intitule
  s.besoin.codesPostes = [code]
  s.modifieLe = le
  s.journal = [
    { date: '2 octobre 2026', texte: `DAR ${s.besoin.darRef} validée par Hélène Robert` },
    { date: le, texte: 'Offre créée — publication non activée' },
    ...(statut === 'publiee' ? [{ date: le, texte: 'Publication activée — 3 canal(aux)' }] : []),
  ]
  return s
}

function dossiersInitiaux(): OffreState[] {
  return [
    etatDarPaie(),
    etatDarRh(),
    etatDarBrouillon(),
    etatSansDar(),
    offreExistante('OFF-2026-0141', 'Chargé·e de mission rénovation énergétique des collectivités', '31-SECL-0412', 'creee', 'Hier, 11:20', 'DAR-2026-0318'),
    offreExistante('OFF-2026-0118', 'Chargé·e de mission mobilité durable', '31-SA-0207', 'publiee', '12 octobre 2026', 'DAR-2026-0274'),
  ]
}

export const dossiers = reactive<OffreState[]>(lire<OffreState[]>(CLE) ?? dossiersInitiaux())

export function ranger(s: OffreState) {
  const i = dossiers.findIndex(d => d.reference === s.reference)
  if (i >= 0) {
    dossiers.splice(i, 1, clone(s))
  }
  else {
    dossiers.unshift(clone(s))
  }
  ecrire(CLE, dossiers)
}

/** Retrouve un recrutement par sa DAR (une DAR = une offre dans ce prototype). */
export function trouverParDar(darRef: string): OffreState | undefined {
  const d = dossiers.find(x => x.besoin.darRef === darRef)
  return d ? clone(d) : undefined
}

export function trouver(reference: string): OffreState | undefined {
  const d = dossiers.find(x => x.reference === reference)
  return d ? clone(d) : undefined
}

export function nouveauDossier(): OffreState {
  const s = etatInitial('dar_csp')
  s.offreDemarree = false
  const max = Math.max(150, ...dossiers.map(d => Number(d.reference.slice(-4)) || 0))
  s.reference = `OFF-2026-${String(max + 1).padStart(4, '0')}`
  s.journal = [{ date: 'Aujourd\'hui', texte: 'Besoin déclaré par Camille Moreau' }]
  return s
}

export function reinitialiserDossiers() {
  dossiers.splice(0, dossiers.length, ...dossiersInitiaux())
  ecrire(CLE, dossiers)
}

// --- Colonnes des tableaux, conservées pendant la session (une configuration par page) ---
export const COLONNES_PAR_DEFAUT = {
  besoins: ['avancement', 'validation', 'postes', 'modifie'],
  offres: ['etat', 'postes', 'limite', 'modifie'],
}
export const colonnes = reactive<Record<'besoins' | 'offres', string[]>>(lire(CLE_COLONNES) ?? { besoins: [...COLONNES_PAR_DEFAUT.besoins], offres: [...COLONNES_PAR_DEFAUT.offres] })
export function enregistrerColonnes() {
  ecrire(CLE_COLONNES, colonnes)
}
