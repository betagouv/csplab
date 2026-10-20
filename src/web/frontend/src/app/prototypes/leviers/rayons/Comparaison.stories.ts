import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { CadragePlancheEcran } from '../CadragePlanche.vue'
import { keepTheme } from '../../keepTheme'
import CadragePlanche from '../CadragePlanche.vue'
import { SOMBRE } from './ecrans'
import { cadreDe, CHAMP_DU_DIALOGUE, IMBRICATIONS } from './imbrications'

const meta = {
  title: 'Prototypes/Leviers/Rayons/Comparaison',
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'kit' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

// The kit, the discreet radii and the assertive radii, with the stories of each: the kit comes with the discreet track
const REGLAGES = [
  { nom: 'Aujourd’hui', prefixe: 'prototypes-leviers-rayons-discrets--kit' },
  { nom: 'Rayons discrets', prefixe: 'prototypes-leviers-rayons-discrets--discrets' },
  { nom: 'Rayons affirmés', prefixe: 'prototypes-leviers-rayons-affirmes--affirmes' },
]

function planche(colonnes: string[], rangees: { legende?: string, ecrans: CadragePlancheEcran[] }[], echelle: number): Story {
  return {
    render: () => ({
      components: { CadragePlanche },
      setup: () => ({ colonnes, rangees, echelle }),
      template: '<CadragePlanche :colonnes="colonnes" :rangees="rangees" :echelle="echelle" />',
    }),
  }
}

// The same cases of the board of nested radii in each setting, enlarged one and a half times; the field of a dialog
// comes from the dialog that adds a step
function imbrications(cas: (number | 'dialogue')[]): Story {
  const colonnes = cas.map(index => index === 'dialogue' ? 'Champ dans un dialogue' : IMBRICATIONS[index]!.legende)
  const rangees = REGLAGES.map(({ nom, prefixe }) => ({
    legende: nom,
    ecrans: cas.map(index => index === 'dialogue'
      ? { story: `${prefixe}-dialogue`, cadre: CHAMP_DU_DIALOGUE }
      : { story: `${prefixe}-imbrications`, cadre: cadreDe(index) }),
  }))
  return planche(colonnes, rangees, 1.5)
}

// The first column of the kanban, from its top to its status footer, in a 1440 x 900 window
const PREMIERE_COLONNE = { x: 295, y: 309, width: 320, height: 565 }
const kanban = planche(
  REGLAGES.map(({ nom }) => nom),
  [{ ecrans: REGLAGES.map(({ prefixe }) => ({ story: prefixe, cadre: PREMIERE_COLONNE })) }],
  1.1,
)

export const Imbrications: Story = { ...imbrications([0, 1, 2, 'dialogue']), name: 'Rayons imbriqués, conteneurs' }
export const ImbricationsControles: Story = { ...imbrications([3, 4, 5, 6]), name: 'Rayons imbriqués, contrôles' }
export const Kanban: Story = kanban
export const KanbanSombre: Story = { ...kanban, name: 'Kanban, sombre', globals: SOMBRE }
