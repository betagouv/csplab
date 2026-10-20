// État de l'offre partagé entre les écrans (provide/inject), règles de complétude,
// circuit de validation et brouillon. Aucune API : tout est simulé en mémoire.

import type { InjectionKey } from 'vue'
import type { Preset } from './scenario'
import type { Contribution, EtapeCircuit, OffreState, Origine, StepId } from './types'
import { computed, inject, nextTick, provide, reactive, ref, watch } from 'vue'
import { ACRONYMES, CANAUX, MOI, personne, SECTIONS_OFFRE } from './referentiels'
import { clone, etatPreset, FICHES } from './scenario'

export interface Manque {
  libelle: string
  stepId: StepId
}

export interface Alerte {
  libelle: string
  stepId: StepId
  niveau: 'info' | 'warning'
}

export type StepStatut = 'complet' | 'incomplet' | 'facultatif' | 'a_faire' | 'en_cours'

export const STEPS: { id: StepId, libelle: string, phase: string, facultatif?: boolean }[] = [
  { id: 'besoin', libelle: 'Besoin et poste', phase: 'Qualifier le besoin' },
  { id: 'poste', libelle: 'Fiche de poste', phase: 'Qualifier le besoin' },
  { id: 'offre', libelle: 'Offre pour les candidats', phase: 'Rédiger l\'offre' },
  { id: 'conditions', libelle: 'Conditions de candidature', phase: 'Préparer le recrutement' },
  { id: 'evaluation', libelle: 'Évaluation des candidatures', phase: 'Préparer le recrutement', facultatif: true },
  { id: 'validation', libelle: 'Validation et équipe', phase: 'Valider et diffuser' },
  { id: 'diffusion', libelle: 'Diffusion', phase: 'Valider et diffuser' },
  { id: 'recap', libelle: 'Récapitulatif', phase: 'Valider et diffuser' },
]

export const LIBELLES_STATUT: Record<OffreState['statut'], { label: string, type: 'info' | 'new' | 'warning' | 'error' | 'success' }> = {
  brouillon: { label: 'Brouillon', type: 'info' },
  a_valider: { label: 'En validation', type: 'new' },
  a_corriger: { label: 'À corriger', type: 'error' },
  validee: { label: 'Validée — prête à publier', type: 'success' },
  publiee: { label: 'Publiée', type: 'success' },
}

const LIBELLES_ORIGINE: Record<Origine, string> = {
  dar: 'Repris de la DAR',
  fiche: 'Repris de la fiche de poste',
  offre: 'Repris de l\'offre dupliquée',
  contribution: 'Ajouté par un contributeur',
}

function getPath(obj: unknown, path: string): unknown {
  return path.split('.').reduce<unknown>((acc, k) => (acc as Record<string, unknown> | undefined)?.[k], obj)
}

function setPath(obj: unknown, path: string, value: unknown) {
  const keys = path.split('.')
  const last = keys.pop()!
  const parent = keys.reduce<unknown>((acc, k) => (acc as Record<string, unknown>)[k], obj) as Record<string, unknown>
  parent[last] = value
}

function vide(v: unknown): boolean {
  if (Array.isArray(v)) {
    return v.length === 0
  }
  return v === null || v === undefined || String(v).trim() === ''
}

function heure(): string {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

let uid = 100
export function nouvelId(prefixe: string): string {
  uid += 1
  return `${prefixe}${uid}`
}

export function createOffre(preset: Preset) {
  const state = reactive<OffreState>(etatPreset(preset))

  const initialStep: StepId | 'demarrer' = {
    nouveau: 'demarrer',
    sans_dar: 'demarrer',
    incomplet: 'poste',
    a_valider: 'validation',
    a_corriger: 'validation',
    pret: 'recap',
  }[preset] as StepId | 'demarrer'
  const step = ref<StepId | 'demarrer'>(initialStep)
  const reprise = ref(preset === 'incomplet' || preset === 'a_corriger')
  watch(() => state.statut, () => (reprise.value = false))
  /** Passe à vrai après une tentative de soumission : les champs requis vides s'affichent en erreur. */
  const afficherErreurs = ref(false)

  // --- Brouillon ---
  const dirty = ref(false)
  const saving = ref(false)
  const lastSaved = ref<string | null>(preset === 'nouveau' || preset === 'sans_dar' ? null : 'il y a 3 jours')
  let ready = false
  watch(() => [state.besoin, state.poste, state.offre, state.conditions, state.evaluation, state.canaux, state.dateLimite, state.dateDebutDiffusion], () => {
    if (ready) {
      dirty.value = true
    }
  }, { deep: true })
  setTimeout(() => {
    ready = true
  }, 0)

  function enregistrer(): Promise<void> {
    saving.value = true
    return new Promise((resolve) => {
      setTimeout(() => {
        saving.value = false
        dirty.value = false
        lastSaved.value = `à ${heure()}`
        resolve()
      }, 700)
    })
  }

  // --- Notification éphémère ---
  const flash = ref<{ texte: string, variant: 'success' | 'info' | 'warning' } | null>(null)
  let flashTimer: ReturnType<typeof setTimeout> | undefined
  function notifier(texte: string, variant: 'success' | 'info' | 'warning' = 'success') {
    flash.value = { texte, variant }
    clearTimeout(flashTimer)
    flashTimer = setTimeout(() => (flash.value = null), 4000)
  }

  function journaliser(texte: string) {
    state.journal.push({ date: `Aujourd'hui, ${heure()}`, texte })
  }

  // --- Origine des valeurs reprises ---
  function origine(path: string): { libelle: string, modifie: boolean } | null {
    const o = state.origines[path]
    if (!o) {
      return null
    }
    const modifie = JSON.stringify(getPath(state, path)) !== JSON.stringify(o.valeur)
    return { libelle: LIBELLES_ORIGINE[o.origine], modifie }
  }

  function restaurer(path: string) {
    const o = state.origines[path]
    if (o) {
      setPath(state, path, clone(o.valeur))
    }
  }

  // --- Complétude ---
  const manques = computed<Manque[]>(() => {
    const m: Manque[] = []
    const b = state.besoin
    const champ = (cond: boolean, libelle: string, stepId: StepId) => {
      if (cond) {
        m.push({ libelle, stepId })
      }
    }
    champ(vide(b.intitule), 'Intitulé du poste', 'besoin')
    champ(vide(b.service), 'Service recruteur', 'besoin')
    champ(vide(b.motif), 'Motif du recrutement', 'besoin')
    champ(vide(b.localisation), 'Localisation', 'besoin')
    champ(vide(b.categories), 'Catégorie(s) du poste', 'besoin')
    champ(vide(b.statuts), 'Statut(s) ouverts au recrutement', 'besoin')
    champ(b.statuts.includes('contractuel') && vide(b.typeContrat), 'Type de contrat proposé aux contractuels', 'besoin')
    champ(b.darApplicable === 'oui' && vide(b.darRef), 'Référence de la DAR', 'besoin')
    champ(vide(state.poste.missions), 'Missions principales', 'poste')
    for (const s of SECTIONS_OFFRE) {
      champ(s.requise && vide(state.offre[s.id].texte), `Section « ${s.libelle} »`, 'offre')
    }
    champ(vide(state.conditions.profils), 'Profils autorisés à candidater', 'conditions')
    champ(!state.canaux.some(c => c.selectionne), 'Au moins un canal de diffusion', 'diffusion')
    champ(vide(state.dateLimite), 'Date limite de candidature', 'diffusion')
    return m
  })

  const alertes = computed<Alerte[]>(() => {
    const a: Alerte[] = []
    const texteOffre = SECTIONS_OFFRE.map(s => state.offre[s.id].texte).join('\n')
    const sigles = ACRONYMES.filter(sigle => new RegExp(`\\b${sigle}\\b`).test(texteOffre))
    if (sigles.length) {
      a.push({ niveau: 'warning', stepId: 'offre', libelle: `Sigles peu compréhensibles pour un candidat : ${sigles.join(', ')}` })
    }
    const reprises = SECTIONS_OFFRE.filter(s => state.offre[s.id].etat === 'reprise')
    if (reprises.length) {
      a.push({ niveau: 'info', stepId: 'offre', libelle: `${reprises.length} section(s) reprise(s) sans retouche : ${reprises.map(s => s.libelle).join(', ')}` })
    }
    if (texteOffre.trim() && !/r[ée]mun[ée]ration|salaire/i.test(texteOffre)) {
      a.push({ niveau: 'warning', stepId: 'offre', libelle: 'La rémunération n\'est pas évoquée (information très attendue par les candidats)' })
    }
    if (texteOffre.length > 4000) {
      a.push({ niveau: 'info', stepId: 'offre', libelle: 'Offre longue (plus de 4 000 caractères) : envisagez de la raccourcir' })
    }
    if (state.besoin.metierHorsReferentiel && !state.besoin.metier) {
      a.push({ niveau: 'info', stepId: 'besoin', libelle: 'Métier hors répertoire : la diffusion sur certains canaux peut demander un métier du répertoire' })
    }
    if (state.conditions.indispensables.length > 5) {
      a.push({ niveau: 'warning', stepId: 'conditions', libelle: 'Plus de 5 critères indispensables : risque d\'écarter de bons profils' })
    }
    for (const q of state.conditions.questions) {
      if (q.bloquante && !q.critereId) {
        a.push({ niveau: 'warning', stepId: 'conditions', libelle: `La question bloquante « ${q.libelle || 'sans libellé'} » n'est rattachée à aucun critère indispensable` })
      }
    }
    for (const r of state.remarques.filter(r => !r.resolue)) {
      a.push({ niveau: 'warning', stepId: r.stepId, libelle: `Remarque de ${personne(r.auteurId).nom} non traitée` })
    }
    return a
  })

  function manquesDe(id: StepId) {
    return manques.value.filter(m => m.stepId === id)
  }

  // --- Circuit de validation ---
  /** L'étape DAR est dérivée du besoin : elle n'existe que si l'organisation en utilise une pour ce poste. */
  const circuit = computed<EtapeCircuit[]>(() => {
    const etapes = [...state.circuit]
    if (state.besoin.darApplicable === 'oui') {
      const validee = state.besoin.darStatut === 'validee'
      etapes.unshift({
        id: 'dar',
        libelle: `Autorisation de recrutement (DAR)${state.besoin.darRef ? ` — ${state.besoin.darRef}` : ''}`,
        personneId: 'helene',
        obligatoire: true,
        statut: validee ? 'approuve' : state.besoin.darStatut === 'en_cours' ? 'en_attente' : 'a_venir',
        date: validee ? '2 octobre 2026' : null,
        externe: validee,
      })
    }
    return etapes
  })

  const validationRestante = computed(() => circuit.value.filter(e => e.obligatoire && e.statut !== 'approuve'))
  const etapeEnCours = computed(() => circuit.value.find(e => e.statut === 'en_attente' || e.statut === 'corrections') ?? null)

  const bloquantsSoumission = computed(() => manques.value.filter(m => m.stepId !== 'diffusion'))
  const peutPublier = computed(() =>
    state.statut !== 'publiee'
    && manques.value.length === 0
    && validationRestante.value.length === 0
    && (state.statut === 'validee' || circuit.value.every(e => !e.obligatoire)),
  )

  const verrouille = computed(() => ['a_valider', 'validee', 'publiee'].includes(state.statut))

  function activerEtapeSuivante() {
    const suivante = state.circuit.find(e => e.statut === 'a_venir' || e.statut === 'corrections')
    if (suivante) {
      suivante.statut = 'en_attente'
      suivante.date = null
    }
  }

  function soumettre(): boolean {
    if (bloquantsSoumission.value.length) {
      afficherErreurs.value = true
      return false
    }
    const resoumission = state.statut === 'a_corriger'
    state.statut = 'a_valider'
    state.remarques.forEach((r) => {
      r.resolue = true
    })
    // Hypothèse : la DAR, quand elle est requise et pas encore obtenue, passe avant les autres validations.
    if (state.besoin.darApplicable === 'oui' && state.besoin.darStatut !== 'validee') {
      state.besoin.darStatut = 'en_cours'
    }
    else {
      activerEtapeSuivante()
    }
    journaliser(resoumission ? 'Corrections apportées, offre soumise à nouveau' : 'Soumise à validation par Camille Moreau')
    if (validationRestante.value.length === 0) {
      state.statut = 'validee'
    }
    void enregistrer()
    notifier(resoumission ? 'Offre renvoyée en validation' : 'Offre soumise à validation')
    return true
  }

  /** Simulation de la réponse d'un valideur (dans la vraie vie : action faite par une autre personne). */
  function repondre(etapeId: string, decision: 'approuve' | 'corrections', remarque?: { texte: string, stepId: StepId }) {
    const nom = personne(circuit.value.find(e => e.id === etapeId)?.personneId ?? '').nom
    if (etapeId === 'dar') {
      if (decision === 'approuve') {
        state.besoin.darStatut = 'validee'
        journaliser(`DAR validée par ${nom}`)
        activerEtapeSuivante()
      }
      else {
        state.besoin.darStatut = 'a_demander'
        state.statut = 'a_corriger'
        journaliser(`DAR refusée ou à revoir (${nom})`)
      }
    }
    else {
      const etape = state.circuit.find(e => e.id === etapeId)!
      etape.statut = decision
      etape.date = `Aujourd'hui, ${heure()}`
      if (decision === 'approuve') {
        journaliser(`Validée par ${nom}`)
        activerEtapeSuivante()
      }
      else {
        state.statut = 'a_corriger'
        journaliser(`Corrections demandées par ${nom}`)
      }
    }
    if (decision === 'corrections' && remarque?.texte) {
      state.remarques.push({ id: nouvelId('r'), auteurId: circuit.value.find(e => e.id === etapeId)?.personneId ?? 'julien', date: `Aujourd'hui, ${heure()}`, texte: remarque.texte, stepId: remarque.stepId, resolue: false })
    }
    if (state.statut === 'a_valider' && validationRestante.value.length === 0) {
      state.statut = 'validee'
      journaliser('Circuit de validation terminé : offre prête à publier')
    }
  }

  function retirerDeValidation() {
    state.statut = 'brouillon'
    state.circuit.forEach((e) => {
      if (e.statut === 'en_attente') {
        e.statut = 'a_venir'
      }
    })
    journaliser('Retirée du circuit de validation pour modification')
    notifier('Offre repassée en brouillon : vous pouvez la modifier', 'info')
  }

  function modifierApresValidation() {
    state.statut = 'brouillon'
    state.circuit.forEach((e) => {
      e.statut = 'a_venir'
      e.date = null
    })
    journaliser('Modification après validation : une nouvelle validation sera nécessaire')
    notifier('Offre repassée en brouillon. Elle devra être validée à nouveau.', 'warning')
  }

  function publier(): boolean {
    if (!peutPublier.value) {
      return false
    }
    state.statut = 'publiee'
    journaliser('Offre publiée')
    void enregistrer()
    return true
  }

  // --- Collaboration ---
  function demanderContribution(c: Omit<Contribution, 'id' | 'statut'>) {
    state.contributions.push({ ...c, id: nouvelId('k'), statut: 'en_attente' })
    journaliser(`Contribution demandée à ${personne(c.personneId).nom}`)
    notifier(`Demande envoyée à ${personne(c.personneId).nom} (notification simulée)`)
  }

  /** Simule le travail du contributeur : complète réellement les champs vides de la fiche de poste. */
  function simulerContribution(id: string) {
    const c = state.contributions.find(k => k.id === id)
    if (!c) {
      return
    }
    c.statut = 'faite'
    const fiche = FICHES[0]!.poste
    if (c.stepId === 'poste') {
      if (!state.poste.competences.length) {
        state.poste.competences = [...fiche.competences!]
        state.origines['poste.competences'] = { origine: 'contribution', valeur: [...fiche.competences!] }
      }
      if (!state.poste.profil) {
        state.poste.profil = fiche.profil!
        state.origines['poste.profil'] = { origine: 'contribution', valeur: fiche.profil }
      }
    }
    journaliser(`${personne(c.personneId).nom} a complété sa contribution`)
    notifier(`${personne(c.personneId).nom} a complété « ${c.demande} »`)
  }

  /** Complète uniquement les champs vides avec la fiche de poste existante ; ne remplace rien. */
  function completerAvecFiche(): number {
    const f = FICHES[0]!
    let n = 0
    for (const [bloc, valeurs] of [['besoin', f.besoin], ['poste', f.poste]] as const) {
      const cible = state[bloc] as unknown as Record<string, unknown>
      for (const [cle, valeur] of Object.entries(valeurs)) {
        if (vide(cible[cle]) && !vide(valeur) && valeur !== false) {
          cible[cle] = clone(valeur)
          state.origines[`${bloc}.${cle}`] = { origine: 'fiche', valeur: clone(valeur) }
          n++
        }
      }
    }
    if (f.poste.aDesConditions && !state.poste.aDesConditions) {
      state.poste.aDesConditions = true
    }
    journaliser(`Complétée avec la fiche de poste ${f.id} (${n} champs vides remplis)`)
    notifier(`${n} champs vides complétés depuis la fiche de poste ${f.id}. Les valeurs déjà saisies n'ont pas été modifiées.`)
    return n
  }

  function statutStep(id: StepId): StepStatut {
    if (id === 'validation') {
      if (state.statut === 'validee' || state.statut === 'publiee') {
        return 'complet'
      }
      return state.statut === 'brouillon' ? 'a_faire' : 'en_cours'
    }
    if (id === 'recap') {
      return manques.value.length === 0 ? 'complet' : 'a_faire'
    }
    if (id === 'evaluation') {
      return state.evaluation.active && state.evaluation.criteres.length ? 'complet' : 'facultatif'
    }
    return manquesDe(id).length ? 'incomplet' : 'complet'
  }

  const progression = computed(() => {
    const comptes = STEPS.filter(s => !s.facultatif && s.id !== 'recap' && s.id !== 'validation')
    const faits = comptes.filter(s => statutStep(s.id) === 'complet').length
    return { faits, total: comptes.length }
  })

  function aller(id: StepId | 'demarrer') {
    step.value = id
    reprise.value = false
    nextTick(() => document.querySelector('.co-main')?.scrollTo({ top: 0 }))
  }

  return {
    state,
    step,
    reprise,
    afficherErreurs,
    dirty,
    saving,
    lastSaved,
    flash,
    enregistrer,
    notifier,
    journaliser,
    origine,
    restaurer,
    manques,
    manquesDe,
    alertes,
    circuit,
    validationRestante,
    etapeEnCours,
    bloquantsSoumission,
    peutPublier,
    verrouille,
    soumettre,
    repondre,
    retirerDeValidation,
    modifierApresValidation,
    publier,
    demanderContribution,
    simulerContribution,
    completerAvecFiche,
    statutStep,
    progression,
    aller,
    moi: MOI,
    canaux: CANAUX,
  }
}

export type OffreStore = ReturnType<typeof createOffre>

const KEY: InjectionKey<OffreStore> = Symbol('offre')

export function provideOffre(preset: Preset): OffreStore {
  const store = createOffre(preset)
  provide(KEY, store)
  return store
}

export function useOffre(): OffreStore {
  const store = inject(KEY)
  if (!store) {
    throw new Error('useOffre() doit être appelé sous provideOffre()')
  }
  return store
}
