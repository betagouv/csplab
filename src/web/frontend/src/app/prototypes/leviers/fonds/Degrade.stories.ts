import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEGRADE, PLANCHE_DEGRADE } from './degrade'
import { ACCUEIL, ETATS_VIDES, fondsMeta, PANNEAU, PARAMETRES, SOMBRE, TELEPHONE } from './ecrans'
import VariantesPlanche from './VariantesPlanche.vue'

const ID = 'prototypes-leviers-fonds-degrade'

const meta = {
  ...fondsMeta(DEGRADE),
  title: 'Prototypes/Leviers/Fonds/Dégradés et textures',
  id: 'prototypes-leviers-fonds-degrade',
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const variantes: Story = {
  render: () => ({
    components: { VariantesPlanche },
    setup: () => ({ planche: PLANCHE_DEGRADE, ecrans: { page: `${ID}--degrade`, panneau: `${ID}--degrade-panneau`, application: `${ID}--degrade` } }),
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

export const Degrade: Story = { name: 'Dégradé et grain, kanban', parameters: { option: 'degrade' } }
export const DegradePanneau: Story = { name: 'Dégradé et grain, panneau', parameters: { option: 'degrade', ...PANNEAU } }
export const DegradeParametres: Story = {
  name: 'Dégradé et grain, paramètres de l’organisme',
  parameters: { option: 'degrade', ...PARAMETRES },
}
export const DegradeEtatsVides: Story = { name: 'Dégradé et grain, états vides', parameters: { option: 'degrade' }, ...ETATS_VIDES }
export const DegradeAccueil: Story = { name: 'Dégradé et grain, accueil', parameters: { option: 'degrade', ...ACCUEIL } }
export const DegradeTelephone: Story = { name: 'Dégradé et grain, téléphone', parameters: { option: 'degrade' }, globals: TELEPHONE }
