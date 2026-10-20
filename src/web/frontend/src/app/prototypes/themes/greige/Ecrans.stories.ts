import type { Meta, StoryObj } from '@storybook/vue3-vite'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import EtatsVidesPlanche from '../../leviers/fonds/EtatsVidesPlanche.vue'
import MouvementScene from '../../leviers/mouvement/MouvementScene.vue'
import { ECRANS } from '../../leviers/ombres/ecrans'
import {
  CHARGEMENT,
  CONFIRMATION,
  DIALOGUE,
  DOCUMENTS,
  ETAPES,
  IMBRICATIONS,
  LISTE,
  MENU,
  MESSAGES,
  NOTES,
  NOTIFICATION,
  PANNEAU,
  PARAMETRES,
  RECRUTEMENT_PATH,
  SOMBRE,
  TELEPHONE,
} from '../../leviers/rayons/ecrans'
import CarteEtats from '../CarteEtats.vue'
import ComposantsPlanche from '../ComposantsPlanche.vue'

// Screens of the application in the greige theme, that the plates of Prototypes/Thèmes/Greige/Planches frame
const meta = {
  title: 'Prototypes/Thèmes/Greige/Écrans',
  id: 'prototypes-themes-greige-ecrans',
  decorators: [keepTheme],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
    viewport: {
      options: { telephone: { name: 'Téléphone, 375 px', styles: { width: '375px', height: '812px' }, type: 'mobile' } },
    },
  },
  globals: { interfaceTheme: 'greige' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

// First candidature of the demo, whose notes and messages are empty
const NOTES_VIDES = { appRoute: `${RECRUTEMENT_PATH}/candidatures/d0000000-0000-4000-8000-000000000001/notes` }
const KIT = { interfaceTheme: 'kit' }

export const Kanban: Story = {}
export const KanbanSombre: Story = { name: 'Kanban, sombre', globals: SOMBRE }
export const Panneau: Story = { name: 'Panneau, notes', parameters: NOTES }
export const PanneauSombre: Story = { name: 'Panneau, notes, sombre', parameters: NOTES, globals: SOMBRE }
export const PanneauCv: Story = { name: 'Panneau, candidature', parameters: PANNEAU }
export const PanneauVide: Story = { name: 'Panneau, notes vides', parameters: NOTES_VIDES }
export const PanneauVideSombre: Story = { name: 'Panneau, notes vides, sombre', parameters: NOTES_VIDES, globals: SOMBRE }
export const Documents: Story = { name: 'Panneau, documents', parameters: DOCUMENTS }
export const Messages: Story = { name: 'Panneau, messages', parameters: MESSAGES }
export const ChangerEtape: Story = { ...ECRANS.panneau, name: 'Panneau, choix de l’étape' }
export const Liste: Story = { parameters: LISTE }
export const ListeSombre: Story = { name: 'Liste, sombre', parameters: LISTE, globals: SOMBRE }
export const Parametres: Story = { name: 'Paramètres de l’organisme', parameters: PARAMETRES }
export const Etapes: Story = { name: 'Étapes de recrutement', parameters: ETAPES }
export const Dialogue: Story = { name: 'Dialogue avec un champ', parameters: ETAPES, ...DIALOGUE }
export const Confirmation: Story = { name: 'Dialogue de confirmation', parameters: ETAPES, ...CONFIRMATION }
export const DialogueSombre: Story = { name: 'Dialogue avec un champ, sombre', parameters: ETAPES, ...DIALOGUE, globals: SOMBRE }
export const Menu: Story = { name: 'Menu ouvert', ...MENU }
export const MenuSombre: Story = { name: 'Menu ouvert, sombre', ...MENU, globals: SOMBRE }
export const Notification: Story = { ...NOTIFICATION }
export const NotificationSombre: Story = { name: 'Notification, sombre', ...NOTIFICATION, globals: SOMBRE }
export const EtatsVides: Story = {
  name: 'États vides',
  render: () => ({ components: { EtatsVidesPlanche }, template: '<EtatsVidesPlanche />' }),
}
export const EtatsVidesSombre: Story = { ...EtatsVides, name: 'États vides, sombre', globals: SOMBRE }
export const Chargement: Story = { ...CHARGEMENT }
export const Composants: Story = {
  render: () => ({ components: { ComposantsPlanche }, template: '<ComposantsPlanche />' }),
}
export const ComposantsSombre: Story = { ...Composants, name: 'Composants, sombre', globals: SOMBRE }
export const Imbrications: Story = { name: 'Rayons imbriqués', ...IMBRICATIONS }
export const ImbricationsSombre: Story = { name: 'Rayons imbriqués, sombre', ...IMBRICATIONS, globals: SOMBRE }
export const Carte: Story = {
  name: 'États de la carte',
  render: () => ({ components: { CarteEtats }, template: '<CarteEtats />' }),
}
export const CarteSombre: Story = { ...Carte, name: 'États de la carte, sombre', globals: SOMBRE }
export const Telephone: Story = { name: 'Téléphone, kanban', globals: TELEPHONE }
export const TelephonePanneau: Story = { name: 'Téléphone, panneau', parameters: NOTES, globals: TELEPHONE }
export const TelephoneSombre: Story = { name: 'Téléphone, kanban, sombre', globals: { ...TELEPHONE, ...SOMBRE } }
export const TelephonePanneauSombre: Story = {
  name: 'Téléphone, panneau, sombre',
  parameters: NOTES,
  globals: { ...TELEPHONE, ...SOMBRE },
}

// The demo of the motion plate, played in a loop on the kanban
export const Scene: Story = {
  name: 'Démonstration du mouvement',
  args: { demo: 'parcours', ralenti: 1 },
  render: (args: Record<string, unknown>) => ({
    components: { MouvementScene },
    setup: () => ({ demo: args.demo, ralenti: Number(args.ralenti) }),
    template: '<MouvementScene :demo="demo" :ralenti="ralenti" />',
  }),
}

// The kit, for the plate that sets the two neutrals side by side
export const KitKanban: Story = { name: 'Aujourd’hui, kanban', globals: KIT }
export const KitKanbanSombre: Story = { name: 'Aujourd’hui, kanban, sombre', globals: { ...KIT, ...SOMBRE } }
