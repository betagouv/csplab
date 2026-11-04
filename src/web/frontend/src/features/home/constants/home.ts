import { ORGANISME_TAB_ROUTE_NAMES, RECRUTEMENTS_TAB_ROUTE_NAMES } from '@/router/names'

export const HELP_URL = 'https://docs.numerique.gouv.fr/docs/53c697f9-ebfb-41f1-bdf2-67a6d29f2db8/'
export const HELP_LABEL = 'Consulter l’aide en ligne'

export interface HomeStep {
  title: string
  description: string
  action?: { label: string, to: string }
}

export const WELCOME_TEXTS: Record<'superviseur' | 'agent', { title: string, description: string, steps: HomeStep[] }> = {
  superviseur: {
    title: 'Prêt à démarrer les recrutements de votre organisme ?',
    description: 'Invitez vos équipes à collaborer sur l’outil pour faire avancer vos recrutements.',
    steps: [
      { title: 'Constituez votre équipe de recrutement', description: 'Invitez les agents qui suivront les candidatures avec vous et choisissez leurs droits d’accès.', action: { label: 'Inviter des membres', to: ORGANISME_TAB_ROUTE_NAMES.membres } },
      { title: 'Définissez le processus de recrutement de votre organisme', description: 'Fixez les étapes par lesquelles passent les candidatures, de la réception jusqu’à la décision.', action: { label: 'Définir les étapes', to: ORGANISME_TAB_ROUTE_NAMES.etapes } },
      { title: 'Assignez un ou des responsables à vos recrutements', description: 'Désignez qui suit chaque recrutement pour que les candidatures avancent sans attendre.', action: { label: 'Voir les recrutements', to: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs } },
    ],
  },
  agent: {
    title: 'Prêt à traiter vos premières candidatures ?',
    description: 'Suivez vos recrutements et coordonnez vos actions avec votre équipe.',
    steps: [
      { title: 'Consultez vos recrutements en cours', description: 'Retrouvez les recrutements auxquels vous participez.', action: { label: 'Voir mes recrutements', to: RECRUTEMENTS_TAB_ROUTE_NAMES.actifs } },
      { title: 'Triez vos candidatures', description: 'Ouvrez un recrutement pour faire avancer ses candidatures d’une étape à l’autre.' },
    ],
  },
}
