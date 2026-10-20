import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ACCUEIL, ETATS_VIDES, fondsMeta, PANNEAU, PARAMETRES, SOMBRE, TELEPHONE } from './ecrans'
import { GREIGE, PLANCHE_GREIGE } from './greige'
import VariantesPlanche from './VariantesPlanche.vue'

const ID = 'prototypes-leviers-fonds-greige'

const meta = {
  ...fondsMeta(GREIGE),
  title: 'Prototypes/Leviers/Fonds/Greige',
  id: 'prototypes-leviers-fonds-greige',
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const variantes: Story = {
  render: () => ({
    components: { VariantesPlanche },
    setup: () => ({ planche: PLANCHE_GREIGE, ecrans: { page: `${ID}--greige`, panneau: `${ID}--greige-discret-panneau`, application: `${ID}--greige` } }),
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

export const Greige: Story = { name: 'Greige classique, kanban', parameters: { option: 'greige' } }
export const GreigePanneau: Story = { name: 'Greige classique, panneau', parameters: { option: 'greige', ...PANNEAU } }
export const GreigeParametres: Story = {
  name: 'Greige classique, paramètres de l’organisme',
  parameters: { option: 'greige', ...PARAMETRES },
}
export const GreigeEtatsVides: Story = { name: 'Greige classique, états vides', parameters: { option: 'greige' }, ...ETATS_VIDES }
export const GreigeAccueil: Story = { name: 'Greige classique, accueil', parameters: { option: 'greige', ...ACCUEIL } }
export const GreigeTelephone: Story = { name: 'Greige classique, téléphone', parameters: { option: 'greige' }, globals: TELEPHONE }

export const GreigeDiscret: Story = { name: 'Greige discret, kanban', parameters: { option: 'greige-discret' } }
export const GreigeDiscretPanneau: Story = {
  name: 'Greige discret, panneau',
  parameters: { option: 'greige-discret', ...PANNEAU },
}
export const GreigeDiscretParametres: Story = {
  name: 'Greige discret, paramètres de l’organisme',
  parameters: { option: 'greige-discret', ...PARAMETRES },
}
export const GreigeDiscretEtatsVides: Story = {
  name: 'Greige discret, états vides',
  parameters: { option: 'greige-discret' },
  ...ETATS_VIDES,
}
export const GreigeDiscretAccueil: Story = {
  name: 'Greige discret, accueil',
  parameters: { option: 'greige-discret', ...ACCUEIL },
}
export const GreigeDiscretTelephone: Story = {
  name: 'Greige discret, téléphone',
  parameters: { option: 'greige-discret' },
  globals: TELEPHONE,
}
