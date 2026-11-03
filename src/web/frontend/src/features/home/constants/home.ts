export const HELP_URL = 'https://docs.numerique.gouv.fr/docs/53c697f9-ebfb-41f1-bdf2-67a6d29f2db8/'
export const HELP_LABEL = 'Consulter l’aide en ligne'

export type HomeLayout = 'tiles' | 'steps'

export type HomeDestination = 'membres' | 'etapes' | 'recrutements'

export interface HomeStep {
  title: string
  description?: string
  tileDescription?: string
  label: string
  icon: string
  action?: string
  to?: HomeDestination
}

export const WELCOME_TEXTS: Record<'superviseur' | 'agent', { title: string, description: string, steps: HomeStep[] }> = {
  superviseur: {
    title: 'Prêt à démarrer les recrutements de votre organisme ?',
    description: 'Invitez vos équipes à collaborer sur l’outil pour faire avancer vos recrutements.',
    steps: [
      { title: 'Constituez votre équipe de recrutement', label: 'Équipe de recrutement', icon: 'ri:account-circle-line', action: 'Inviter des membres', to: 'membres' },
      { title: 'Définissez le processus de recrutement de votre organisme', label: 'Processus de recrutement', icon: 'ri:table-line', action: 'Définir les étapes', to: 'etapes' },
      { title: 'Assignez un ou des responsables à vos recrutements', label: 'Recrutements', icon: 'ri:briefcase-line', action: 'Voir les recrutements', to: 'recrutements' },
    ],
  },
  agent: {
    title: 'Prêt à traiter vos premières candidatures ?',
    description: 'Suivez vos recrutements et coordonnez vos actions avec votre équipe.',
    steps: [
      { title: 'Consultez vos recrutements en cours', tileDescription: 'Consultez vos recrutements en cours et triez vos candidatures', label: 'Mes recrutements', icon: 'ri:briefcase-line', action: 'Voir mes recrutements', to: 'recrutements' },
      { title: 'Triez vos candidatures', description: 'Ouvrez un recrutement pour faire avancer ses candidatures d’une étape à l’autre.', label: 'Candidatures', icon: 'ri:layout-column-line' },
    ],
  },
}
