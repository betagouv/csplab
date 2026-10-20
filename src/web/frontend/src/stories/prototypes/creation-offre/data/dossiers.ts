// Dossiers de la session du prototype : simule le serveur. Rangés dans sessionStorage pour survivre
// à un rechargement de page (l'irritant « rafraîchissement toutes les 5 minutes » des outils actuels).

import type { OffreState } from './types'
import { reactive } from 'vue'
import { clone, etatInitial, etatPreset } from './scenario'

const CLE = 'csplab-proto-creation-offre-dossiers-v3'
const CLE_COLONNES = 'csplab-proto-creation-offre-colonnes-v3'

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

function dossiersInitiaux(): OffreState[] {
  const soumise = etatPreset('a_valider')
  soumise.reference = 'OFF-2026-0141'
  soumise.modifieLe = 'Hier, 11:20'
  soumise.besoin.codesPostes = ['31-SECL-0412']
  const aCorriger = etatPreset('a_corriger')
  aCorriger.reference = 'OFF-2026-0139'
  aCorriger.besoin.intitule = 'Chargé·e d\'études énergie-climat'
  aCorriger.besoin.codesPostes = ['31-SECL-0388']
  aCorriger.modifieLe = 'Hier, 17:44'
  const publiee = etatPreset('pret')
  publiee.reference = 'OFF-2026-0118'
  publiee.statut = 'publiee'
  publiee.besoin.intitule = 'Chargé·e de mission mobilité durable'
  publiee.besoin.codesPostes = ['31-SA-0207']
  publiee.modifieLe = '12 octobre 2026'
  publiee.journal.push({ date: '12 octobre 2026', texte: 'Offre publiée' })
  return [etatPreset('paie'), soumise, aCorriger, publiee]
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

export function trouver(reference: string): OffreState | undefined {
  const d = dossiers.find(x => x.reference === reference)
  return d ? clone(d) : undefined
}

export function nouveauDossier(): OffreState {
  const s = etatInitial()
  const max = Math.max(150, ...dossiers.map(d => Number(d.reference.slice(-4)) || 0))
  s.reference = `OFF-2026-${String(max + 1).padStart(4, '0')}`
  s.journal = [{ date: 'Aujourd\'hui', texte: 'Dossier créé par Camille Moreau' }]
  return s
}

export function reinitialiserDossiers() {
  dossiers.splice(0, dossiers.length, ...dossiersInitiaux())
  ecrire(CLE, dossiers)
}

// --- Colonnes du tableau, conservées pendant la session ---
export const COLONNES_PAR_DEFAUT = ['reference', 'intitule', 'postes', 'statut', 'modifie']
export const colonnes = reactive<{ visibles: string[] }>({ visibles: lire<string[]>(CLE_COLONNES) ?? [...COLONNES_PAR_DEFAUT] })
export function enregistrerColonnes() {
  ecrire(CLE_COLONNES, colonnes.visibles)
}
