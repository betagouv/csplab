// Moteur du formulaire décrit en données (piste 2 : principe de survey-kit, sans dépendance).
// La description a deux parties : `reponses` (une entrée par réponse : type, libellé, choix, obligatoire, conditions)
// et `questionnaire` (parties → étapes → pages → questions placées). Ce fichier lit la description, vérifie
// qu'elle tient debout, évalue les conditions d'affichage et calcule l'avancement. L'affichage est dans les .vue.

export type TypeReponse
  = | 'texte' | 'url' | 'nombre' | 'texte-long' | 'date'
    | 'choix' | 'choix-multiple' | 'oui-non' | 'interrupteur'
    | 'liste-texte' | 'repetable'

export const TYPES: TypeReponse[] = ['texte', 'url', 'nombre', 'texte-long', 'date', 'choix', 'choix-multiple', 'oui-non', 'interrupteur', 'liste-texte', 'repetable']

export interface Choix {
  valeur: string
  libelle: string
  /** Valeur de la réponse `filtrePar` pour laquelle ce choix est proposé. */
  parent?: string
  /** Données attachées, reprises par `preRempliPar` (ex. compétences d'un métier). */
  donnees?: Record<string, unknown>
}

export interface Reponse {
  type: TypeReponse
  libelle: string
  obligatoire?: boolean
  aide?: string
  placeholder?: string
  defaut?: unknown
  /** `choix` en liste déroulante (par défaut), en boutons radio ou en sélecteur segmenté. */
  affichage?: 'liste' | 'radio' | 'segments'
  /** Chaînes (valeur = libellé) ou objets. */
  choix?: (string | Partial<Choix> & { valeur: string })[]
  /** Condition d'affichage, ex. `natureEmploi = contractuel || natureEmploi = les_deux`, `!sansLieuFixe`. */
  visibleSi?: string
  /** Les choix proposés dépendent de la réponse à cette question (via `parent`). */
  filtrePar?: string
  /** Si la question parente est vide : tout proposer, ou désactiver le champ. */
  siParentVide?: 'tout' | 'desactive'
  texteParentVide?: string
  /** Quand la question source change, la réponse reprend `donnees[donnee]` du choix fait. */
  preRempliPar?: { question: string, donnee: string }
  /** Libellé du bouton d'ajout (liste-texte, repetable). */
  ajouter?: string
  /** Sous-questions d'un élément répétable. */
  champs?: Record<string, Reponse>
}

export interface Placement {
  id: string
  largeur?: 'pleine' | 'demi' | 'tiers'
}
export interface Page {
  id: string
  titre?: string
  description?: string
  questions: (string | Placement)[]
}
export interface Etape {
  id: string
  titre: string
  aide?: string
  pages: Page[]
}
export interface Partie {
  id: string
  titre: string
  aide?: string
  etapes: Etape[]
}
export interface Description {
  id: string
  version?: string
  titre?: string
  note?: string
  reponses: Record<string, Reponse>
  questionnaire: { parties: Partie[] }
}

export type Valeur = string | boolean | string[] | Record<string, string>[]
export type Reponses = Record<string, Valeur>

// ——— Lecture et vérification ———

/** Lit un texte JSON et renvoie la description, ou la liste des problèmes trouvés (en français, pour l'éditeur). */
export function lireDescription(texte: string): { description?: Description, erreurs: string[] } {
  let brut: unknown
  try {
    brut = JSON.parse(texte)
  }
  catch (e) {
    return { erreurs: [`JSON invalide : ${(e as Error).message}`] }
  }
  return verifier(brut)
}

export function verifier(brut: unknown): { description?: Description, erreurs: string[] } {
  const erreurs: string[] = []
  const d = brut as Partial<Description>
  if (!d || typeof d !== 'object' || !d.reponses || typeof d.reponses !== 'object') {
    return { erreurs: ['Il manque l\'objet « reponses ».'] }
  }
  if (!Array.isArray(d.questionnaire?.parties)) {
    return { erreurs: ['Il manque « questionnaire.parties » (une liste).'] }
  }
  const ids = new Set(Object.keys(d.reponses))
  for (const [id, r] of Object.entries(d.reponses)) {
    verifierReponse(id, r, ids, erreurs)
  }
  const placees = new Set<string>()
  for (const p of d.questionnaire.parties) {
    if (!Array.isArray(p.etapes)) {
      erreurs.push(`Partie « ${p.id} » : il manque « etapes ».`)
      continue
    }
    for (const e of p.etapes) {
      if (!Array.isArray(e.pages)) {
        erreurs.push(`Étape « ${e.id} » : il manque « pages ».`)
        continue
      }
      for (const pg of e.pages) {
        for (const q of pg.questions ?? []) {
          const qid = typeof q === 'string' ? q : q?.id
          if (!ids.has(qid)) {
            erreurs.push(`Étape « ${e.id} » : la question « ${qid} » n'existe pas dans « reponses ».`)
          }
          if (placees.has(qid)) {
            erreurs.push(`La question « ${qid} » est placée deux fois.`)
          }
          placees.add(qid)
        }
      }
    }
  }
  return erreurs.length ? { erreurs } : { description: d as Description, erreurs }
}

function verifierReponse(id: string, r: Reponse, ids: Set<string>, erreurs: string[]) {
  if (!TYPES.includes(r?.type)) {
    erreurs.push(`« ${id} » : type inconnu « ${r?.type} » (types possibles : ${TYPES.join(', ')}).`)
    return
  }
  if (!r.libelle) {
    erreurs.push(`« ${id} » : il manque « libelle ».`)
  }
  if ((r.type === 'choix' || r.type === 'choix-multiple') && !Array.isArray(r.choix)) {
    erreurs.push(`« ${id} » : une question à choix a besoin de « choix ».`)
  }
  if (r.visibleSi) {
    try {
      for (const ref of referencesCondition(r.visibleSi)) {
        if (!ids.has(ref)) {
          erreurs.push(`« ${id} » : la condition cite « ${ref} », qui n'existe pas.`)
        }
      }
    }
    catch (e) {
      erreurs.push(`« ${id} » : condition illisible — ${(e as Error).message}`)
    }
  }
  if (r.filtrePar && !ids.has(r.filtrePar)) {
    erreurs.push(`« ${id} » : « filtrePar » cite « ${r.filtrePar} », qui n'existe pas.`)
  }
  if (r.preRempliPar && !ids.has(r.preRempliPar.question)) {
    erreurs.push(`« ${id} » : « preRempliPar » cite « ${r.preRempliPar.question} », qui n'existe pas.`)
  }
  if (r.type === 'repetable') {
    if (!r.champs || typeof r.champs !== 'object') {
      erreurs.push(`« ${id} » : un élément répétable a besoin de « champs ».`)
    }
    else {
      for (const [sid, s] of Object.entries(r.champs)) {
        if (!['texte', 'choix'].includes(s?.type)) {
          erreurs.push(`« ${id}.${sid} » : dans un répétable, seuls « texte » et « choix » sont pris en charge.`)
        }
      }
    }
  }
}

// ——— Conditions d'affichage ———
// Syntaxe proche de survey-kit : `a = x`, `a != x`, `a > 3`, `a.includes(x)`, `a.excludes(x)`, `a` (rempli),
// `!a` (vide), combinés par `&&` (prioritaire) et `||`. Pas de parenthèses.

const ATOME = /^(!?)(\w+)(?:\.(includes|excludes)\((.*)\)|\s*(!=|>=|<=|[=><])\s*(\S.*))?$/

function sansGuillemets(v: string) {
  return v.trim().replace(/^(['"])(.*)\1$/, '$2')
}

function lireAtome(a: string) {
  const m = ATOME.exec(a.trim())
  if (!m) {
    throw new Error(`« ${a.trim()} » n'est pas compris`)
  }
  return { non: m[1] === '!', id: m[2]!, fonction: m[3], argument: m[4], op: m[5], valeur: m[6] }
}

function morceaux(expr: string): string[][] {
  return expr.split('||').map(ou => ou.split('&&'))
}

export function referencesCondition(expr: string): string[] {
  return [...new Set(morceaux(expr).flat().map(a => lireAtome(a).id))]
}

export function rempli(v: unknown): boolean {
  if (Array.isArray(v)) {
    return v.length > 0
  }
  if (typeof v === 'boolean') {
    return v
  }
  return v !== undefined && v !== null && String(v).trim() !== ''
}

function evaluerAtome(a: string, rep: Reponses): boolean {
  const { non, id, fonction, argument, op, valeur } = lireAtome(a)
  const v = rep[id]
  let res: boolean
  if (fonction) {
    const x = sansGuillemets(argument ?? '')
    const dedans = Array.isArray(v) ? (v as unknown[]).includes(x) : String(v ?? '').includes(x)
    res = fonction === 'includes' ? dedans : !dedans
  }
  else if (op) {
    const x = sansGuillemets(valeur ?? '')
    if (op === '=' || op === '!=') {
      const egal = Array.isArray(v) ? (v as unknown[]).includes(x) : String(v ?? '') === x
      res = op === '=' ? egal : !egal
    }
    else {
      const n = Number(v)
      const m = Number(x)
      res = op === '>' ? n > m : op === '>=' ? n >= m : op === '<' ? n < m : n <= m
    }
  }
  else {
    res = rempli(v)
  }
  return non ? !res : res
}

export function evaluer(expr: string | undefined, rep: Reponses): boolean {
  if (!expr) {
    return true
  }
  try {
    return morceaux(expr).some(et => et.every(a => evaluerAtome(a, rep)))
  }
  catch {
    return true
  }
}

// ——— Choix, valeurs, dépendances ———

export function choixDe(r: Reponse): Choix[] {
  return (r.choix ?? []).map(c => (typeof c === 'string' ? { valeur: c, libelle: c } : { ...c, libelle: c.libelle ?? c.valeur }))
}

/** Choix proposés compte tenu des autres réponses (`filtrePar`). `null` = champ désactivé (parent vide). */
export function choixProposes(r: Reponse, rep: Reponses): Choix[] | null {
  const tous = choixDe(r)
  if (!r.filtrePar) {
    return tous
  }
  const p = rep[r.filtrePar]
  const parents = (Array.isArray(p) ? p : [p]).filter(rempli).map(String)
  if (!parents.length) {
    return r.siParentVide === 'desactive' ? null : tous
  }
  const vus = new Set<string>()
  return tous.filter(c => (!c.parent || parents.includes(c.parent)) && !vus.has(c.valeur) && vus.add(c.valeur))
}

export function valeurInitiale(r: Reponse): Valeur {
  if (r.defaut !== undefined) {
    return structuredClone(r.defaut) as Valeur
  }
  switch (r.type) {
    case 'choix-multiple':
    case 'liste-texte':
    case 'repetable':
      return []
    case 'interrupteur':
      return false
    default:
      return ''
  }
}

/** Réponses de départ. Garde les réponses déjà données quand la description change (même id, même type). */
export function reponsesInitiales(d: Description, avant?: Reponses, typesAvant?: Record<string, TypeReponse>): Reponses {
  const rep: Reponses = {}
  for (const [id, r] of Object.entries(d.reponses)) {
    rep[id] = avant && id in avant && typesAvant?.[id] === r.type ? avant[id]! : valeurInitiale(r)
  }
  return nettoyer(d, rep)
}

/** Retire les choix qui ne sont plus proposés (ex. grades d'un corps retiré, métier d'une autre famille). Renvoie les réponses modifiées. */
function retirerChoixPerimes(d: Description, rep: Reponses): string[] {
  const modifiees: string[] = []
  for (const [id, r] of Object.entries(d.reponses)) {
    if (!r.filtrePar) {
      continue
    }
    const ok = new Set((choixProposes(r, rep) ?? []).map(c => c.valeur))
    const v = rep[id]
    if (Array.isArray(v)) {
      const garde = (v as string[]).filter(x => ok.has(x))
      if (garde.length !== v.length) {
        rep[id] = garde
        modifiees.push(id)
      }
    }
    else if (typeof v === 'string' && v && !ok.has(v)) {
      rep[id] = ''
      modifiees.push(id)
    }
  }
  return modifiees
}

/** Pré-remplit les réponses qui dépendent de `id` (ex. compétences du métier). Renvoie les réponses modifiées. */
function preRemplir(d: Description, rep: Reponses, id: string): string[] {
  const modifiees: string[] = []
  for (const [cible, r] of Object.entries(d.reponses)) {
    if (r.preRempliPar?.question === id) {
      const source = d.reponses[id]
      const c = source ? choixDe(source).find(x => x.valeur === rep[id]) : undefined
      const v = c?.donnees?.[r.preRempliPar.donnee]
      rep[cible] = Array.isArray(v) ? [...v as string[]] : valeurInitiale(r)
      modifiees.push(cible)
    }
  }
  return modifiees
}

/** Applique les dépendances en cascade (catégorie → corps → grades, famille → métier → compétences). */
function propager(d: Description, rep: Reponses, depart: string[]) {
  let aTraiter = depart
  for (let tour = 0; tour < 10; tour++) {
    const suivantes = [...aTraiter.flatMap(id => preRemplir(d, rep, id)), ...retirerChoixPerimes(d, rep)]
    if (!suivantes.length) {
      return
    }
    aTraiter = suivantes
  }
}

export function nettoyer(d: Description, rep: Reponses): Reponses {
  propager(d, rep, [])
  return rep
}

/** Enregistre une réponse puis applique les dépendances (pré-remplissage, puis nettoyage des choix). */
export function repondre(d: Description, rep: Reponses, id: string, valeur: Valeur) {
  rep[id] = valeur
  propager(d, rep, [id])
}

// ——— Visibilité et avancement ———

export function placement(q: string | Placement): Placement {
  return typeof q === 'string' ? { id: q } : q
}

export function visible(d: Description, id: string, rep: Reponses): boolean {
  return evaluer(d.reponses[id]?.visibleSi, rep)
}

/** Une question obligatoire est remplie ; pour un répétable, chaque élément a ses sous-champs obligatoires remplis. */
export function complete(r: Reponse, v: Valeur | undefined): boolean {
  if (r.type === 'repetable') {
    const items = (v ?? []) as Record<string, string>[]
    return items.every(it => Object.entries(r.champs ?? {}).every(([k, s]) => !s.obligatoire || rempli(it[k])))
  }
  if (r.type === 'liste-texte') {
    return (v as string[] | undefined ?? []).some(x => x.trim())
  }
  return rempli(v)
}

/** Une question compte comme obligatoire si elle est affichée et marquée `obligatoire`. Un répétable compte dès qu'il a un élément. */
function compte(r: Reponse, v: Valeur | undefined): boolean {
  if (r.type === 'repetable') {
    return Array.isArray(v) && v.length > 0 && Object.values(r.champs ?? {}).some(s => s.obligatoire)
  }
  return Boolean(r.obligatoire)
}

export function questionsEtape(e: Etape): string[] {
  return e.pages.flatMap(p => p.questions.map(q => placement(q).id))
}

export function obligatoiresEtape(d: Description, e: Etape, rep: Reponses): { id: string, libelle: string, ok: boolean }[] {
  return questionsEtape(e)
    .filter(id => d.reponses[id] && visible(d, id, rep) && compte(d.reponses[id]!, rep[id]))
    .map(id => ({ id, libelle: d.reponses[id]!.libelle, ok: complete(d.reponses[id]!, rep[id]) }))
}

export function etapesDe(d: Description): (Etape & { partie: Partie })[] {
  return d.questionnaire.parties.flatMap(p => (p.etapes ?? []).map(e => ({ ...e, partie: p })))
}

/** Réponses envoyées : seulement les questions affichées (une question masquée n'a pas de réponse). */
export function reponsesVisibles(d: Description, rep: Reponses): Reponses {
  const sortie: Reponses = {}
  for (const id of etapesDe(d).flatMap(questionsEtape)) {
    if (d.reponses[id] && visible(d, id, rep) && id in rep) {
      sortie[id] = rep[id]!
    }
  }
  return sortie
}

export function nombreConditions(d: Description): number {
  return Object.values(d.reponses).filter(r => r.visibleSi || r.filtrePar || r.preRempliPar).length
}
