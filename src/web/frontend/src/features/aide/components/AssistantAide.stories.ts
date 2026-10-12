import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import type { FaqEntree } from '../types'
import { FAQ_ENTREES } from '../constants/faq'
import { MESSAGE_SANS_REPONSE } from '../utils/motsClesAdapter'
import AssistantAide from './AssistantAide.vue'

type AssistantAideProps = ComponentPropsAndSlots<typeof AssistantAide>

function entreeFaq(id: string): FaqEntree {
  const entree = FAQ_ENTREES.find(candidate => candidate.id === id)
  if (!entree) {
    throw new Error(`Entrée de FAQ introuvable : ${id}`)
  }
  return entree
}

const ENTREE_TROUVEE = entreeFaq('cand-etape-suivante')

const meta = {
  title: 'Compositions/ATS/AssistantAide',
  component: AssistantAide,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
    controls: {
      include: ['pending'],
    },
    docs: {
      description: {
        component: 'Bloc de réponse de l\'assistant de la page Aide : entrée de FAQ la plus proche de la question, avec son emplacement dans l\'application. Purement présentationnel — la page lui passe la réponse de `useAssistantAide`.',
      },
    },
  },
}

export default meta
type Story = StoryObj<AssistantAideProps>

export const ReponseTrouvee: Story = {
  name: 'Réponse trouvée',
  args: {
    pending: false,
    reponse: { reponse: ENTREE_TROUVEE.reponse, entreeId: ENTREE_TROUVEE.id },
  },
}

export const AucuneEntree: Story = {
  name: 'Aucune entrée ne se détache',
  args: {
    pending: false,
    reponse: { reponse: MESSAGE_SANS_REPONSE, entreeId: null },
  },
}

export const RechercheEnCours: Story = {
  name: 'Recherche en cours',
  args: {
    pending: true,
  },
}

export const Erreur: Story = {
  args: {
    pending: false,
    error: new Error('Assistant indisponible'),
  },
}
