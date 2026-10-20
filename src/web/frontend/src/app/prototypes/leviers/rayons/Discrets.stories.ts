import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DISCRETS } from './discrets'
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
  ...rayonsMeta(DISCRETS),
  title: 'Prototypes/Leviers/Rayons/Rayons discrets',
  id: 'prototypes-leviers-rayons-discrets',
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

export const Discrets: Story = { name: 'Rayons discrets, kanban', parameters: { option: 'discrets' } }
export const DiscretsPanneau: Story = {
  name: 'Rayons discrets, panneau',
  parameters: { option: 'discrets', ...PANNEAU },
}
export const DiscretsNotes: Story = {
  name: 'Rayons discrets, notes du panneau',
  parameters: { option: 'discrets', ...NOTES },
}
export const DiscretsDocuments: Story = {
  name: 'Rayons discrets, documents du panneau',
  parameters: { option: 'discrets', ...DOCUMENTS },
}
export const DiscretsMessages: Story = {
  name: 'Rayons discrets, messages du panneau',
  parameters: { option: 'discrets', ...MESSAGES },
}
export const DiscretsListe: Story = { name: 'Rayons discrets, liste', parameters: { option: 'discrets', ...LISTE } }
export const DiscretsParametres: Story = {
  name: 'Rayons discrets, paramètres de l’organisme',
  parameters: { option: 'discrets', ...PARAMETRES },
}
export const DiscretsEtapes: Story = {
  name: 'Rayons discrets, étapes de recrutement',
  parameters: { option: 'discrets', ...ETAPES },
}
export const DiscretsDialogue: Story = {
  name: 'Rayons discrets, dialogue avec un champ',
  parameters: { option: 'discrets', ...ETAPES },
  ...DIALOGUE,
}
export const DiscretsConfirmation: Story = {
  name: 'Rayons discrets, dialogue de confirmation',
  parameters: { option: 'discrets', ...ETAPES },
  ...CONFIRMATION,
}
export const DiscretsMenu: Story = { name: 'Rayons discrets, menu ouvert', parameters: { option: 'discrets' }, ...MENU }
export const DiscretsNotification: Story = {
  name: 'Rayons discrets, notification',
  parameters: { option: 'discrets' },
  ...NOTIFICATION,
}
export const DiscretsChargement: Story = {
  name: 'Rayons discrets, chargement',
  parameters: { option: 'discrets' },
  ...CHARGEMENT,
}
export const DiscretsComposants: Story = {
  name: 'Rayons discrets, composants',
  parameters: { option: 'discrets' },
  ...COMPOSANTS,
}
export const DiscretsImbrications: Story = {
  name: 'Rayons discrets, imbrications',
  parameters: { option: 'discrets' },
  ...IMBRICATIONS,
}
export const DiscretsTelephone: Story = {
  name: 'Rayons discrets, téléphone',
  parameters: { option: 'discrets' },
  globals: TELEPHONE,
}
export const DiscretsTelephonePanneau: Story = {
  name: 'Rayons discrets, panneau sur téléphone',
  parameters: { option: 'discrets', ...PANNEAU },
  globals: TELEPHONE,
}
export const DiscretsSombre: Story = {
  name: 'Rayons discrets, kanban, sombre',
  parameters: { option: 'discrets' },
  globals: SOMBRE,
}
export const DiscretsNotesSombre: Story = {
  name: 'Rayons discrets, notes du panneau, sombre',
  parameters: { option: 'discrets', ...NOTES },
  globals: SOMBRE,
}
