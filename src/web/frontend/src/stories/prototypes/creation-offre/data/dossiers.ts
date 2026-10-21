// Dossiers de la session du prototype : simule le serveur. Rangés dans sessionStorage pour survivre
// à un rechargement de page (l'irritant « rafraîchissement toutes les 5 minutes » des outils actuels).

import type { FichePoste, OffreState } from './types'
import { reactive } from 'vue'
import { rangerFiche, reinitialiserFiches, trouverFiche } from './fiches'
import { clone, etatDarBrouillon, etatDarRh, etatInitial, etatPreset, etatSansDar } from './scenario'

const CLE = 'csplab-proto-creation-offre-dossiers-v6'
const CLE_COLONNES = 'csplab-proto-creation-offre-colonnes-v6'

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

/** Recrutements de démonstration, chacun rattaché à une fiche du référentiel. */
function dossiersInitiaux(): OffreState[] {
  const lier = (s: OffreState, reference: string, ficheId: string, version: string) => {
    s.reference = reference
    s.ficheId = ficheId
    s.ficheVersion = version
    s.besoin.ficheRef = ficheId
    return s
  }
  return [
    lier(etatDarRh(), 'REC-2026-0152', 'FP-SG-2026-003', '16 octobre 2026'),
    lier(etatDarBrouillon(), 'REC-2026-0153', 'FP-SG-2026-011', dateLongue('Hier')),
    lier(etatSansDar(), 'REC-2026-0154', 'FP-SG-2026-014', '18 octobre 2026'),
    lier(offreExistante('REC-2026-0141', 'Chargé·e de mission rénovation énergétique des collectivités', '31-SECL-0412', 'creee', 'Hier, 11:20', 'DAR-2026-0318'), 'REC-2026-0141', 'FP-SECL-2024-012', '14 mai 2024'),
    lier(offreExistante('REC-2026-0118', 'Chargé·e de mission mobilité durable', '31-SA-0207', 'publiee', '12 octobre 2026', 'DAR-2026-0274'), 'REC-2026-0118', 'FP-SECL-2023-004', '9 janvier 2026'),
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
  const max = Math.max(155, ...dossiers.map(d => Number(d.reference.slice(-4)) || 0))
  s.reference = `REC-2026-${String(max + 1).padStart(4, '0')}`
  s.journal = [{ date: 'Aujourd\'hui', texte: 'Besoin déclaré par Camille Moreau' }]
  return s
}

export function reinitialiserDossiers() {
  dossiers.splice(0, dossiers.length, ...dossiersInitiaux())
  ecrire(CLE, dossiers)
  reinitialiserFiches()
}

/** « Aujourd'hui, 10:20 » / « Hier » → date en toutes lettres, pour dire « version du … ». */
function dateLongue(d: string): string {
  const jour = new Date()
  if (d.startsWith('Hier')) {
    jour.setDate(jour.getDate() - 1)
  }
  else if (!d.startsWith('Aujourd')) {
    return d
  }
  return jour.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

/** Référence de l'offre d'un recrutement (même numéro, préfixe distinct). */
export function refOffre(s: OffreState): string {
  return s.reference.replace('REC-', 'OFF-')
}

/**
 * Lance un recrutement depuis une fiche. Les informations sont **copiées** : modifier la fiche ensuite
 * ne change ni la DAR ni l'offre de ce recrutement.
 */
export function lancerRecrutement(f: FichePoste, parcours: 'dar' | 'direct', nbPostes: string): OffreState {
  const s = etatInitial('dar_csp')
  const max = Math.max(155, ...dossiers.map(d => Number(d.reference.slice(-4)) || 0))
  s.reference = `REC-2026-${String(max + 1).padStart(4, '0')}`
  s.ficheId = f.id
  s.ficheVersion = dateLongue(f.modifieLe)
  s.modifieLe = `Aujourd'hui, ${new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`
  Object.assign(s.besoin, {
    intitule: f.intitule,
    organisme: f.organisme,
    service: f.service,
    localisation: f.localisation,
    teletravail: f.teletravail,
    categories: [...f.categories],
    statuts: [...f.statuts],
    metier: f.metier,
    corps: f.corps,
    ficheRef: f.id,
    nbPostes,
    codesPostes: [],
  })
  Object.assign(s.poste, {
    missions: f.missions,
    activites: [...f.activites],
    competences: [...f.competences],
    qualifications: f.qualifications,
    profil: f.profil,
    environnement: f.environnement,
    aDesConditions: Boolean(f.conditionsParticulieres),
    conditionsParticulieres: f.conditionsParticulieres,
  })
  s.titreAnnonce = f.intitule
  s.canaux.forEach((c) => {
    c.selectionne = c.id === 'csp'
  })
  const postes = `${nbPostes} poste${Number(nbPostes) > 1 ? 's' : ''}`
  if (parcours === 'dar') {
    s.besoin.darApplicable = 'oui'
    s.besoin.darRef = `DAR-2026-0${340 + dossiers.length}`
    s.besoin.darStatut = 'a_demander'
    s.offreDemarree = false
  }
  else {
    s.besoin.darApplicable = 'non'
    s.offreDemarree = true
  }
  s.journal = [{ date: `Aujourd'hui, ${new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`, texte: `Recrutement lancé depuis la fiche ${f.id} (${postes}) — ${parcours === 'dar' ? 'avec DAR' : 'création directe de l\'offre'}` }]
  s.derniereEtape = parcours === 'dar' ? 'poste' : 'candidature'
  ranger(s)
  const fiche = trouverFiche(f.id)
  if (fiche) {
    fiche.journal.push({ date: 'Aujourd\'hui', texte: `Recrutement ${s.reference} lancé (${postes})` })
    rangerFiche(fiche)
  }
  return s
}

export function recrutementsDe(ficheId: string): OffreState[] {
  return dossiers.filter(d => d.ficheId === ficheId)
}

// --- Colonnes des tableaux, conservées pendant la session (une configuration par page) ---
export const COLONNES_PAR_DEFAUT = {
  recrutements: ['fiche', 'avancement', 'parcours', 'postes', 'modifie'],
  offres: ['etat', 'postes', 'limite', 'modifie'],
}
export const colonnes = reactive<Record<'recrutements' | 'offres', string[]>>(lire(CLE_COLONNES) ?? { recrutements: [...COLONNES_PAR_DEFAUT.recrutements], offres: [...COLONNES_PAR_DEFAUT.offres] })
export function enregistrerColonnes() {
  ecrire(CLE_COLONNES, colonnes)
}
