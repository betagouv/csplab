import type { Meta, StoryObj } from '@storybook/vue3-vite'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import { ETATS_VIDES } from '../../leviers/fonds/ecrans'
import { ECRANS as OMBRES } from '../../leviers/ombres/ecrans'
import {
  CHARGEMENT,
  CONFIRMATION,
  DIALOGUE,
  DOCUMENTS,
  ETAPES,
  LISTE,
  MENU,
  MESSAGES,
  NOTES,
  NOTIFICATION,
  PANNEAU,
  PARAMETRES,
  RECRUTEMENT_PATH,
  TELEPHONE,
} from '../../leviers/rayons/ecrans'

// Screens of the application in the theme, which the plates of the theme frame
const meta = {
  title: 'Prototypes/Thèmes/La Suite/Écrans',
  id: 'prototypes-themes-lasuite-ecrans',
  decorators: [keepTheme],
  parameters: {
    layout: 'fullscreen',
    appRoute: RECRUTEMENT_PATH,
    viewport: {
      options: { telephone: { name: 'Téléphone, 375 px', styles: { width: '375px', height: '812px' }, type: 'mobile' } },
    },
  },
  globals: { interfaceTheme: 'lasuite' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const SOMBRE = { interfaceTheme: 'lasuite', theme: 'dark' }

export const Kanban: Story = {}
export const KanbanSombre: Story = { name: 'Kanban, sombre', globals: SOMBRE }
export const Panneau: Story = { name: 'Panneau, CV', parameters: PANNEAU }
export const Notes: Story = { name: 'Panneau, notes', parameters: NOTES }
export const NotesSombre: Story = { name: 'Panneau, notes, sombre', parameters: NOTES, globals: SOMBRE }
export const Documents: Story = { name: 'Panneau, documents', parameters: DOCUMENTS }
export const Messages: Story = { name: 'Panneau, messages', parameters: MESSAGES }
export const MessagesSombre: Story = { name: 'Panneau, messages, sombre', parameters: MESSAGES, globals: SOMBRE }
export const ChoixEtape: Story = { ...OMBRES.panneau, name: 'Panneau, choix de l’étape' }
export const ChoixEtapeSombre: Story = { ...OMBRES.panneau, name: 'Panneau, choix de l’étape, sombre', globals: SOMBRE }
export const Liste: Story = { parameters: LISTE }
export const ListeSombre: Story = { name: 'Liste, sombre', parameters: LISTE, globals: SOMBRE }
export const Parametres: Story = { name: 'Paramètres de l’organisme', parameters: PARAMETRES }
export const ParametresSombre: Story = { name: 'Paramètres de l’organisme, sombre', parameters: PARAMETRES, globals: SOMBRE }
export const Etapes: Story = { name: 'Étapes du recrutement', parameters: ETAPES }
export const Dialogue: Story = { name: 'Dialogue avec un champ', parameters: ETAPES, ...DIALOGUE }
export const DialogueSombre: Story = { name: 'Dialogue avec un champ, sombre', parameters: ETAPES, globals: SOMBRE, ...DIALOGUE }
export const Confirmation: Story = { name: 'Dialogue de confirmation', parameters: ETAPES, ...CONFIRMATION }
export const Refus: Story = { ...OMBRES.dialogue, name: 'Dialogue du motif de refus' }
export const Menu: Story = { name: 'Menu ouvert', ...MENU }
export const MenuSombre: Story = { name: 'Menu ouvert, sombre', globals: SOMBRE, ...MENU }
export const Notification: Story = { ...NOTIFICATION }
export const NotificationSombre: Story = { name: 'Notification, sombre', globals: SOMBRE, ...NOTIFICATION }
export const EtatsVides: Story = { name: 'États vides', ...ETATS_VIDES }
export const EtatsVidesSombre: Story = { name: 'États vides, sombre', globals: SOMBRE, ...ETATS_VIDES }
export const Chargement: Story = { ...CHARGEMENT }
export const ChargementSombre: Story = { name: 'Chargement, sombre', globals: SOMBRE, ...CHARGEMENT }
export const Telephone: Story = { name: 'Téléphone', globals: { interfaceTheme: 'lasuite', ...TELEPHONE } }
export const TelephonePanneau: Story = {
  name: 'Téléphone, panneau',
  parameters: NOTES,
  globals: { interfaceTheme: 'lasuite', ...TELEPHONE },
}
export const TelephoneSombre: Story = { name: 'Téléphone, sombre', globals: { ...SOMBRE, ...TELEPHONE } }
export const TelephonePanneauSombre: Story = {
  name: 'Téléphone, panneau, sombre',
  parameters: NOTES,
  globals: { ...SOMBRE, ...TELEPHONE },
}
