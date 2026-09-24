import type { InjectionKey } from 'vue'
import type { CandidatureEspace, ConversationEspace, JeuDonnees, PieceJointe, Utilisateur } from './espaceMock'
import { computed, inject, provide, reactive } from 'vue'
import { creerCandidaturesMock, creerUtilisateurMock, statutMeta } from './espaceMock'
import { MAINTENANT_REFERENCE } from './format'

export interface OptionsEspace {
  jeu: JeuDonnees
  methode: Utilisateur['methode']
  // Fait échouer la toute première tentative d'envoi de message, pour montrer « Réessayer ».
  simulerEchecEnvoi: boolean
}

// État frais à chaque montage de l'espace (plutôt qu'un module global) : évite qu'un retrait ou
// un message envoyé dans une story ne fuite dans les suivantes.
export function creerEspace(options: OptionsEspace) {
  const candidatures = reactive<CandidatureEspace[]>(creerCandidaturesMock(options.jeu))
  const utilisateur = reactive<Utilisateur>(creerUtilisateurMock(options.methode))

  let horloge = 0
  const maintenant = () => new Date(MAINTENANT_REFERENCE.getTime() + (++horloge) * 60_000)

  const parActivite = (a: CandidatureEspace, b: CandidatureEspace) =>
    b.derniereActivite.getTime() - a.derniereActivite.getTime()

  const enCours = computed(() =>
    candidatures.filter(c => statutMeta[c.statut].enCours).sort(parActivite),
  )
  const terminees = computed(() =>
    candidatures.filter(c => !statutMeta[c.statut].enCours).sort(parActivite),
  )

  function candidature(id: string): CandidatureEspace | undefined {
    return candidatures.find(c => c.id === id)
  }

  function nonLusConversation(conversation: ConversationEspace): number {
    return conversation.messages.filter(m => !m.lu && m.auteur === 'recruteur').length
  }

  function nonLusCandidature(c: CandidatureEspace): number {
    return c.conversations.reduce((total, conv) => total + nonLusConversation(conv), 0)
  }

  const nonLusTotal = computed(() =>
    candidatures.reduce((total, c) => total + nonLusCandidature(c), 0),
  )

  function conversationsTriees(candidatureId: string): ConversationEspace[] {
    const c = candidature(candidatureId)
    if (!c) {
      return []
    }
    const dernier = (conv: ConversationEspace) => conv.messages.at(-1)?.date.getTime() ?? 0
    return [...c.conversations].sort((a, b) => dernier(b) - dernier(a))
  }

  function marquerConversationLue(candidatureId: string, conversationId: string) {
    candidature(candidatureId)
      ?.conversations
      .find(conv => conv.id === conversationId)
      ?.messages
      .forEach((m) => { m.lu = true })
  }

  function envoyerMessage(candidatureId: string, conversationId: string, texte: string, pieces: PieceJointe[]) {
    const c = candidature(candidatureId)
    const conversation = c?.conversations.find(conv => conv.id === conversationId)
    if (!c || !conversation) {
      return
    }
    const date = maintenant()
    conversation.messages.push({
      id: `m-${conversation.messages.length + 1}-${date.getTime()}`,
      auteur: 'candidat',
      texte,
      date,
      lu: true,
      pieces,
    })
    c.derniereActivite = date
  }

  // Retrait irréversible : statut « Retirée », bascule dans Terminées, événement au journal.
  function retirer(candidatureId: string, motif?: string) {
    const c = candidature(candidatureId)
    if (!c) {
      return
    }
    const date = maintenant()
    c.statut = 'retiree'
    c.derniereActivite = date
    c.journal.push({ date, texte: 'Candidature retirée par le candidat', motif })
  }

  return {
    options,
    utilisateur,
    candidatures,
    enCours,
    terminees,
    nonLusTotal,
    candidature,
    conversationsTriees,
    nonLusConversation,
    nonLusCandidature,
    marquerConversationLue,
    envoyerMessage,
    retirer,
  }
}

export type Espace = ReturnType<typeof creerEspace>

const cle: InjectionKey<Espace> = Symbol('espace-candidat')

export function provideEspace(espace: Espace): void {
  provide(cle, espace)
}

export function useEspace(): Espace {
  const espace = inject(cle)
  if (!espace) {
    throw new Error('useEspace() doit être appelé sous un composant qui a fait provideEspace()')
  }
  return espace
}
