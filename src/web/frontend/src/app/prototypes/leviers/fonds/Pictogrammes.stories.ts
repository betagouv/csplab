import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ACCUEIL, ETATS_VIDES, fondsMeta, PANNEAU, PARAMETRES, SOMBRE, TELEPHONE } from './ecrans'
import { PICTOGRAMMES, PLANCHE_PICTOGRAMMES } from './pictogrammes'
import VariantesPlanche from './VariantesPlanche.vue'

const ID = 'prototypes-leviers-fonds-pictogrammes'

const meta = {
  ...fondsMeta(PICTOGRAMMES),
  title: 'Prototypes/Leviers/Fonds/Pictogrammes',
  id: 'prototypes-leviers-fonds-pictogrammes',
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const variantes: Story = {
  render: () => ({
    components: { VariantesPlanche },
    setup: () => ({
      planche: PLANCHE_PICTOGRAMMES,
      ecrans: { page: `${ID}--pictogrammes`, panneau: `${ID}--pictogrammes-panneau`, application: `${ID}--pictogrammes` },
    }),
    template: '<VariantesPlanche :planche="planche" :ecrans="ecrans" />',
  }),
}

export const Variantes: Story = variantes
export const VariantesSombre: Story = { ...variantes, name: 'Variantes, sombre', globals: SOMBRE }

export const Kit: Story = { name: 'Kit actuel, kanban', parameters: { option: 'kit' } }
export const KitPanneau: Story = { name: 'Kit actuel, panneau', parameters: { option: 'kit', ...PANNEAU } }
export const KitParametres: Story = { name: 'Kit actuel, paramètres de l’organisme', parameters: { option: 'kit', ...PARAMETRES } }
export const KitEtatsVides: Story = { name: 'Kit actuel, états vides', parameters: { option: 'kit' }, ...ETATS_VIDES }
export const KitAccueil: Story = { name: 'Kit actuel, accueil', parameters: { option: 'kit', ...ACCUEIL } }
export const KitTelephone: Story = { name: 'Kit actuel, téléphone', parameters: { option: 'kit' }, globals: TELEPHONE }

export const Pictogrammes: Story = { name: 'Pictogrammes classiques, kanban', parameters: { option: 'pictogrammes' } }
export const PictogrammesPanneau: Story = {
  name: 'Pictogrammes classiques, panneau',
  parameters: { option: 'pictogrammes', ...PANNEAU },
}
export const PictogrammesParametres: Story = {
  name: 'Pictogrammes classiques, paramètres de l’organisme',
  parameters: { option: 'pictogrammes', ...PARAMETRES },
}
export const PictogrammesEtatsVides: Story = {
  name: 'Pictogrammes classiques, états vides',
  parameters: { option: 'pictogrammes' },
  ...ETATS_VIDES,
}
export const PictogrammesAccueil: Story = {
  name: 'Pictogrammes classiques, accueil',
  parameters: { option: 'pictogrammes', ...ACCUEIL },
}
export const PictogrammesTelephone: Story = {
  name: 'Pictogrammes classiques, téléphone',
  parameters: { option: 'pictogrammes' },
  globals: TELEPHONE,
}

export const PictogrammesDiscret: Story = { name: 'Pictogrammes discrets, kanban', parameters: { option: 'pictogrammes-discret' } }
export const PictogrammesDiscretPanneau: Story = {
  name: 'Pictogrammes discrets, panneau',
  parameters: { option: 'pictogrammes-discret', ...PANNEAU },
}
export const PictogrammesDiscretParametres: Story = {
  name: 'Pictogrammes discrets, paramètres de l’organisme',
  parameters: { option: 'pictogrammes-discret', ...PARAMETRES },
}
export const PictogrammesDiscretEtatsVides: Story = {
  name: 'Pictogrammes discrets, états vides',
  parameters: { option: 'pictogrammes-discret' },
  ...ETATS_VIDES,
}
export const PictogrammesDiscretAccueil: Story = {
  name: 'Pictogrammes discrets, accueil',
  parameters: { option: 'pictogrammes-discret', ...ACCUEIL },
}
export const PictogrammesDiscretTelephone: Story = {
  name: 'Pictogrammes discrets, téléphone',
  parameters: { option: 'pictogrammes-discret' },
  globals: TELEPHONE,
}
