import type { Meta } from '@storybook/vue3-vite'
import { ECRANS, OMBRES_META } from './ecrans'

const meta = {
  ...OMBRES_META,
  title: 'Prototypes/Leviers/Ombres/Ombres du DSFR',
  id: 'prototypes-leviers-ombres-dsfr',
  parameters: { ...OMBRES_META.parameters, option: 'dsfr' },
} satisfies Meta

export default meta

export const Etats = ECRANS.etats
export const EtatsSombre = ECRANS.etatsSombre
export const Kanban = ECRANS.kanban
export const Menu = ECRANS.menu
export const Panneau = ECRANS.panneau
export const PanneauSombre = ECRANS.panneauSombre
export const Dialogue = ECRANS.dialogue
export const Etapes = ECRANS.etapes
