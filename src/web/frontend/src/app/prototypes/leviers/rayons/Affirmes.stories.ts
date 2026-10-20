import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { RAYONS_AFFIRMES } from './affirmes'
import {
  CHARGEMENT,
  COMPOSANTS,
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
  rayonsMeta,
  SOMBRE,
  TELEPHONE,
} from './ecrans'

const meta = {
  ...rayonsMeta(RAYONS_AFFIRMES),
  title: 'Prototypes/Leviers/Rayons/Rayons affirmés',
  id: 'prototypes-leviers-rayons-affirmes',
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

export const Kit: Story = { name: 'Kit actuel, kanban', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...PANNEAU } }
export const KitNotes: Story = { name: 'Kit actuel, notes du panneau', parameters: { option: 'kit', ...NOTES } }
export const KitDocuments: Story = {
  name: 'Kit actuel, documents du panneau',
  parameters: { option: 'kit', ...DOCUMENTS },
}
export const KitMessages: Story = {
  name: 'Kit actuel, messages du panneau',
  parameters: { option: 'kit', ...MESSAGES },
}
export const KitListe: Story = { name: 'Kit actuel, liste', parameters: { option: 'kit', ...LISTE } }
export const KitParametres: Story = {
  name: 'Kit actuel, paramètres de l’organisme',
  parameters: { option: 'kit', ...PARAMETRES },
}
export const KitEtapes: Story = { name: 'Kit actuel, étapes de recrutement', parameters: { option: 'kit', ...ETAPES } }
export const KitDialogue: Story = {
  name: 'Kit actuel, dialogue avec un champ',
  parameters: { option: 'kit', ...ETAPES },
  ...DIALOGUE,
}
export const KitConfirmation: Story = {
  name: 'Kit actuel, dialogue de confirmation',
  parameters: { option: 'kit', ...ETAPES },
  ...CONFIRMATION,
}
export const KitMenu: Story = { name: 'Kit actuel, menu ouvert', parameters: { option: 'kit' }, ...MENU }
export const KitNotification: Story = {
  name: 'Kit actuel, notification',
  parameters: { option: 'kit' },
  ...NOTIFICATION,
}
export const KitChargement: Story = { name: 'Kit actuel, chargement', parameters: { option: 'kit' }, ...CHARGEMENT }
export const KitComposants: Story = { name: 'Kit actuel, composants', parameters: { option: 'kit' }, ...COMPOSANTS }
export const KitImbrications: Story = {
  name: 'Kit actuel, imbrications',
  parameters: { option: 'kit' },
  ...IMBRICATIONS,
}
export const KitTelephone: Story = { name: 'Kit actuel, téléphone', parameters: { option: 'kit' }, globals: TELEPHONE }
export const KitTelephonePanneau: Story = {
  name: 'Kit actuel, panneau sur téléphone',
  parameters: { option: 'kit', ...PANNEAU },
  globals: TELEPHONE,
}
export const KitSombre: Story = { name: 'Kit actuel, kanban, sombre', parameters: { option: 'kit' }, globals: SOMBRE }
export const KitNotesSombre: Story = {
  name: 'Kit actuel, notes du panneau, sombre',
  parameters: { option: 'kit', ...NOTES },
  globals: SOMBRE,
}

export const Affirmes: Story = { name: 'Rayons affirmés, kanban', parameters: { option: 'affirmes' } }
export const AffirmesPanneau: Story = {
  name: 'Rayons affirmés, panneau',
  parameters: { option: 'affirmes', ...PANNEAU },
}
export const AffirmesNotes: Story = {
  name: 'Rayons affirmés, notes du panneau',
  parameters: { option: 'affirmes', ...NOTES },
}
export const AffirmesDocuments: Story = {
  name: 'Rayons affirmés, documents du panneau',
  parameters: { option: 'affirmes', ...DOCUMENTS },
}
export const AffirmesMessages: Story = {
  name: 'Rayons affirmés, messages du panneau',
  parameters: { option: 'affirmes', ...MESSAGES },
}
export const AffirmesListe: Story = { name: 'Rayons affirmés, liste', parameters: { option: 'affirmes', ...LISTE } }
export const AffirmesParametres: Story = {
  name: 'Rayons affirmés, paramètres de l’organisme',
  parameters: { option: 'affirmes', ...PARAMETRES },
}
export const AffirmesEtapes: Story = {
  name: 'Rayons affirmés, étapes de recrutement',
  parameters: { option: 'affirmes', ...ETAPES },
}
export const AffirmesDialogue: Story = {
  name: 'Rayons affirmés, dialogue avec un champ',
  parameters: { option: 'affirmes', ...ETAPES },
  ...DIALOGUE,
}
export const AffirmesConfirmation: Story = {
  name: 'Rayons affirmés, dialogue de confirmation',
  parameters: { option: 'affirmes', ...ETAPES },
  ...CONFIRMATION,
}
export const AffirmesMenu: Story = { name: 'Rayons affirmés, menu ouvert', parameters: { option: 'affirmes' }, ...MENU }
export const AffirmesNotification: Story = {
  name: 'Rayons affirmés, notification',
  parameters: { option: 'affirmes' },
  ...NOTIFICATION,
}
export const AffirmesChargement: Story = {
  name: 'Rayons affirmés, chargement',
  parameters: { option: 'affirmes' },
  ...CHARGEMENT,
}
export const AffirmesComposants: Story = {
  name: 'Rayons affirmés, composants',
  parameters: { option: 'affirmes' },
  ...COMPOSANTS,
}
export const AffirmesImbrications: Story = {
  name: 'Rayons affirmés, imbrications',
  parameters: { option: 'affirmes' },
  ...IMBRICATIONS,
}
export const AffirmesTelephone: Story = {
  name: 'Rayons affirmés, téléphone',
  parameters: { option: 'affirmes' },
  globals: TELEPHONE,
}
export const AffirmesTelephonePanneau: Story = {
  name: 'Rayons affirmés, panneau sur téléphone',
  parameters: { option: 'affirmes', ...PANNEAU },
  globals: TELEPHONE,
}
export const AffirmesSombre: Story = {
  name: 'Rayons affirmés, kanban, sombre',
  parameters: { option: 'affirmes' },
  globals: SOMBRE,
}
export const AffirmesNotesSombre: Story = {
  name: 'Rayons affirmés, notes du panneau, sombre',
  parameters: { option: 'affirmes', ...NOTES },
  globals: SOMBRE,
}
