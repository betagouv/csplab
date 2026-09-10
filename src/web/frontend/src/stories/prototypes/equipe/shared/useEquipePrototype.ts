import type { Persona, ProtoAgent, ProtoEvenement, ProtoRecrutement, RoleOffre, RoleOrganisme } from '../data/mock'
import { computed, reactive, ref, watch } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import { createScenario, minutesAgo, nextUuid, PERSONAS, ROLE_OFFRE_LABELS, ROLE_ORGANISME_LABELS } from '../data/mock'
import { formatAgentNom, formatListe } from './format'

export type RecrutementTab = 'equipe' | 'etapes' | 'activite'
export type OrganismeTab = 'membres' | 'etapes' | 'journal'

export type ProtoPage
  = | { name: 'recrutements' }
    | { name: 'parametres-recrutement', recrutementUuid: string, tab: RecrutementTab }
    | { name: 'parametres-organisme', tab: OrganismeTab }

export interface InvitationPayload {
  prenom: string
  nom: string
  email: string
  poste: string
}

const NAVIGATION_DELAY_MS = 250

export function useEquipePrototype(initialPersona: Persona, initialPage: ProtoPage = { name: 'recrutements' }) {
  const scenario = reactive(createScenario())
  const { addToast } = useToast()

  const persona = ref<Persona>(initialPersona)
  const page = ref<ProtoPage>(initialPage)
  const pending = ref(false)
  const assignation = ref<string[] | null>(null)

  const utilisateur = computed(() => PERSONAS[persona.value])
  const agentCourant = computed(() => scenario.agents.find(a => a.uuid === utilisateur.value.agentUuid) ?? null)
  const isAdmin = computed(() => persona.value === 'admin')
  const isGestionnaire = computed(() => agentCourant.value?.roleOrganisme === 'gestionnaire')

  const peutGererOrganisme = computed(() => isAdmin.value || isGestionnaire.value)
  const peutPromouvoirGestionnaire = computed(() => isAdmin.value)
  const peutAssignerResponsables = computed(() => isAdmin.value || isGestionnaire.value)

  function agentOf(uuid: string): ProtoAgent | null {
    return scenario.agents.find(a => a.uuid === uuid) ?? null
  }

  function recrutementOf(uuid: string): ProtoRecrutement | null {
    return scenario.recrutements.find(r => r.uuid === uuid) ?? null
  }

  function roleSur(recrutementUuid: string): RoleOffre | null {
    const agent = agentCourant.value
    if (!agent)
      return null
    return recrutementOf(recrutementUuid)?.membres.find(m => m.agentUuid === agent.uuid)?.roleOffre ?? null
  }

  function peutGererEquipe(recrutementUuid: string): boolean {
    return peutAssignerResponsables.value || roleSur(recrutementUuid) === 'responsable'
  }

  const recrutementsVisibles = computed(() =>
    scenario.recrutements.filter(r => peutAssignerResponsables.value || roleSur(r.uuid) !== null),
  )

  const sansRecrutement = computed(() => !peutAssignerResponsables.value && recrutementsVisibles.value.length === 0)

  const gestionnaires = computed(() => scenario.agents.filter(a => a.roleOrganisme === 'gestionnaire'))

  function responsablesDe(recrutement: ProtoRecrutement): ProtoAgent[] {
    return recrutement.membres
      .filter(m => m.roleOffre === 'responsable')
      .map(m => agentOf(m.agentUuid))
      .filter((a): a is ProtoAgent => a !== null)
  }

  const recrutementsSansResponsable = computed(() =>
    scenario.recrutements.filter(r => !r.archive && responsablesDe(r).length === 0),
  )

  let navigationTimer: ReturnType<typeof setTimeout> | undefined

  function naviguer(next: ProtoPage): void {
    clearTimeout(navigationTimer)
    page.value = next
    pending.value = true
    navigationTimer = setTimeout(() => {
      pending.value = false
    }, NAVIGATION_DELAY_MS)
  }

  function goRecrutements(): void {
    naviguer({ name: 'recrutements' })
  }

  function goParametresRecrutement(recrutementUuid: string, tab: RecrutementTab = 'equipe'): void {
    naviguer({ name: 'parametres-recrutement', recrutementUuid, tab })
  }

  function goParametresOrganisme(tab: OrganismeTab = 'membres'): void {
    naviguer({ name: 'parametres-organisme', tab })
  }

  function pageAccessible(target: ProtoPage): boolean {
    if (target.name === 'parametres-organisme')
      return peutGererOrganisme.value
    if (target.name === 'parametres-recrutement')
      return recrutementsVisibles.value.some(r => r.uuid === target.recrutementUuid)
    return true
  }

  watch(persona, () => {
    assignation.value = null
    if (!pageAccessible(page.value))
      naviguer({ name: 'recrutements' })
  })

  function demanderAssignation(recrutementUuids: string[]): void {
    assignation.value = recrutementUuids
  }

  function auteur(): string {
    return utilisateur.value.nom
  }

  function tracerOffre(recrutementUuid: string, libelle: string): void {
    scenario.activitesOffres.unshift({ uuid: nextUuid('evt'), recrutementUuid, date: minutesAgo(0), auteur: auteur(), libelle })
    const recrutement = recrutementOf(recrutementUuid)
    if (recrutement)
      recrutement.derniereActivite = minutesAgo(0)
  }

  function tracerOrganisme(libelle: string): void {
    scenario.journalOrganisme.unshift({ uuid: nextUuid('log'), date: minutesAgo(0), auteur: auteur(), libelle })
  }

  function parDateDecroissante(a: ProtoEvenement, b: ProtoEvenement): number {
    return b.date.localeCompare(a.date)
  }

  function activitesDe(recrutementUuid: string): ProtoEvenement[] {
    return scenario.activitesOffres.filter(e => e.recrutementUuid === recrutementUuid).sort(parDateDecroissante)
  }

  const journalOrganisme = computed(() => [...scenario.journalOrganisme].sort(parDateDecroissante))

  function ajouterMembre(recrutementUuid: string, agentUuid: string, roleOffre: RoleOffre, fonction: string | null): void {
    const recrutement = recrutementOf(recrutementUuid)
    const agent = agentOf(agentUuid)
    if (!recrutement || !agent || recrutement.membres.some(m => m.agentUuid === agentUuid))
      return
    recrutement.membres.push({ agentUuid, roleOffre, fonction })
    tracerOffre(recrutementUuid, `a ajouté ${formatAgentNom(agent)} comme ${ROLE_OFFRE_LABELS[roleOffre].toLowerCase()}`)
    addToast({
      variant: 'success',
      title: 'Membre ajouté',
      description: `${formatAgentNom(agent)} rejoint l'équipe comme ${ROLE_OFFRE_LABELS[roleOffre].toLowerCase()}. Un courriel l'en informe.`,
    })
  }

  function modifierRoleOffre(recrutementUuid: string, agentUuid: string, roleOffre: RoleOffre): void {
    const membre = recrutementOf(recrutementUuid)?.membres.find(m => m.agentUuid === agentUuid)
    const agent = agentOf(agentUuid)
    if (!membre || !agent || membre.roleOffre === roleOffre)
      return
    membre.roleOffre = roleOffre
    tracerOffre(recrutementUuid, `a passé ${formatAgentNom(agent)} ${ROLE_OFFRE_LABELS[roleOffre].toLowerCase()}`)
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatAgentNom(agent)} est maintenant ${ROLE_OFFRE_LABELS[roleOffre].toLowerCase()} sur cette offre.`,
    })
  }

  function retirerMembre(recrutementUuid: string, agentUuid: string): void {
    const recrutement = recrutementOf(recrutementUuid)
    const agent = agentOf(agentUuid)
    if (!recrutement || !agent)
      return
    recrutement.membres = recrutement.membres.filter(m => m.agentUuid !== agentUuid)
    tracerOffre(recrutementUuid, `a retiré ${formatAgentNom(agent)} de l'équipe`)
    addToast({
      variant: 'success',
      title: 'Membre retiré',
      description: `${formatAgentNom(agent)} n'a plus accès à cette offre.`,
    })
  }

  function inviterALaVolee(payload: InvitationPayload, recrutementUuid: string | null, roleOrganisme: RoleOrganisme = 'agent'): ProtoAgent {
    const agent: ProtoAgent = {
      uuid: nextUuid('agent'),
      prenom: payload.prenom.trim(),
      nom: payload.nom.trim(),
      email: payload.email.trim().toLowerCase(),
      poste: payload.poste.trim(),
      roleOrganisme,
      statut: 'en_attente',
      dateCreation: minutesAgo(0),
      dateDerniereActivite: null,
    }
    scenario.agents.push(agent)
    const recrutement = recrutementUuid ? recrutementOf(recrutementUuid) : null
    tracerOrganisme(`a créé le compte de ${formatAgentNom(agent)} (${ROLE_ORGANISME_LABELS[roleOrganisme].toLowerCase()})${recrutement ? ` depuis l'offre « ${recrutement.intitule} »` : ''}`)
    if (!recrutement) {
      addToast({
        variant: 'success',
        title: 'Compte créé',
        description: `${formatAgentNom(agent)} recevra un courriel d'invitation à ${agent.email}.`,
      })
    }
    return agent
  }

  function assignerResponsable(recrutementUuids: string[], agentUuid: string, fonction: string | null = null): void {
    const agent = agentOf(agentUuid)
    if (!agent)
      return
    const intitules: string[] = []
    for (const uuid of recrutementUuids) {
      const recrutement = recrutementOf(uuid)
      if (!recrutement)
        continue
      const membre = recrutement.membres.find(m => m.agentUuid === agentUuid)
      if (membre) {
        membre.roleOffre = 'responsable'
        membre.fonction = fonction ?? membre.fonction
      }
      else {
        recrutement.membres.push({ agentUuid, roleOffre: 'responsable', fonction })
      }
      tracerOffre(uuid, `a désigné ${formatAgentNom(agent)} responsable de l'offre`)
      intitules.push(recrutement.intitule)
    }
    const count = intitules.length
    addToast({
      variant: 'success',
      title: count > 1 ? `Responsable assigné sur ${count} offres` : 'Responsable assigné',
      description: `${formatAgentNom(agent)} pilote maintenant ${count > 1 ? 'ces offres' : `« ${intitules[0]} »`}. Un courriel l'en informe.`,
    })
  }

  function modifierRoleOrganisme(agentUuid: string, roleOrganisme: RoleOrganisme): void {
    const agent = agentOf(agentUuid)
    if (!agent || agent.roleOrganisme === roleOrganisme)
      return
    agent.roleOrganisme = roleOrganisme
    tracerOrganisme(`a passé ${formatAgentNom(agent)} ${ROLE_ORGANISME_LABELS[roleOrganisme].toLowerCase()}`)
    addToast({
      variant: 'success',
      title: 'Rôle modifié',
      description: `${formatAgentNom(agent)} est maintenant ${ROLE_ORGANISME_LABELS[roleOrganisme].toLowerCase()} de l'organisme.`,
    })
  }

  function revoquer(agentUuid: string): void {
    const agent = agentOf(agentUuid)
    if (!agent)
      return
    scenario.agents = scenario.agents.filter(a => a.uuid !== agentUuid)
    const offres: string[] = []
    for (const recrutement of scenario.recrutements) {
      if (recrutement.membres.some(m => m.agentUuid === agentUuid)) {
        recrutement.membres = recrutement.membres.filter(m => m.agentUuid !== agentUuid)
        tracerOffre(recrutement.uuid, `a révoqué ${formatAgentNom(agent)} de l'organisme, retiré de l'équipe`)
        offres.push(recrutement.intitule)
      }
    }
    tracerOrganisme(`a révoqué les accès de ${formatAgentNom(agent)}${offres.length ? ` (retiré de ${formatListe(offres.map(o => `« ${o} »`))})` : ''}`)
    addToast({
      variant: 'success',
      title: 'Accès révoqués',
      description: `${formatAgentNom(agent)} n'a plus accès à l'organisme ni à ses recrutements.`,
    })
  }

  function renvoyerInvitation(agentUuid: string): void {
    const agent = agentOf(agentUuid)
    if (!agent)
      return
    tracerOrganisme(`a renvoyé l'invitation à ${formatAgentNom(agent)}`)
    addToast({
      variant: 'success',
      title: 'Invitation renvoyée',
      description: `Un nouveau courriel a été envoyé à ${agent.email}.`,
    })
  }

  return {
    scenario,
    persona,
    page,
    pending,
    assignation,
    utilisateur,
    agentCourant,
    isAdmin,
    isGestionnaire,
    peutGererOrganisme,
    peutPromouvoirGestionnaire,
    peutAssignerResponsables,
    peutGererEquipe,
    roleSur,
    agentOf,
    recrutementOf,
    responsablesDe,
    recrutementsVisibles,
    recrutementsSansResponsable,
    sansRecrutement,
    gestionnaires,
    activitesDe,
    journalOrganisme,
    naviguer,
    goRecrutements,
    goParametresRecrutement,
    goParametresOrganisme,
    demanderAssignation,
    ajouterMembre,
    modifierRoleOffre,
    retirerMembre,
    inviterALaVolee,
    assignerResponsable,
    modifierRoleOrganisme,
    revoquer,
    renvoyerInvitation,
  }
}

export type EquipePrototype = ReturnType<typeof useEquipePrototype>
