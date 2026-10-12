import type { FAQ_THEMES } from './constants/faq'

export interface FaqEntree {
  id: string
  theme: (typeof FAQ_THEMES)[number]
  question: string
  reponse: string
  ou: string
  motsCles: string[]
}

export interface ReponseAide {
  reponse: string
  entreeId: string | null
}

export interface AssistantAdapter {
  repondre: (question: string) => Promise<ReponseAide>
}
