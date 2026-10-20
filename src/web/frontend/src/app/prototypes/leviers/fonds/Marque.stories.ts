import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { ACCUEIL, ETATS_VIDES, fondsMeta, INTROUVABLE, PANNEAU, PARAMETRES, SOMBRE, TELEPHONE } from './ecrans'
import { MARQUE, PLANCHE_MARQUE } from './marque'
import VariantesPlanche from './VariantesPlanche.vue'

const ID = 'prototypes-leviers-fonds-marque'

const meta = {
  ...fondsMeta(MARQUE),
  title: 'Prototypes/Leviers/Fonds/Motif de l’identité de csplab',
  id: 'prototypes-leviers-fonds-marque',
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

const variantes: Story = {
  render: () => ({
    components: { VariantesPlanche },
    setup: () => ({ planche: PLANCHE_MARQUE, ecrans: { page: `${ID}--marque-introuvable`, panneau: `${ID}--marque-panneau`, application: `${ID}--marque` } }),
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
export const KitIntrouvable: Story = { name: 'Kit actuel, page introuvable', parameters: { option: 'kit', ...INTROUVABLE } }

export const Marque: Story = { name: 'Motif de l’identité, kanban', parameters: { option: 'marque' } }
export const MarquePanneau: Story = { name: 'Motif de l’identité, panneau', parameters: { option: 'marque', ...PANNEAU } }
export const MarqueParametres: Story = {
  name: 'Motif de l’identité, paramètres de l’organisme',
  parameters: { option: 'marque', ...PARAMETRES },
}
export const MarqueEtatsVides: Story = { name: 'Motif de l’identité, états vides', parameters: { option: 'marque' }, ...ETATS_VIDES }
export const MarqueAccueil: Story = { name: 'Motif de l’identité, accueil', parameters: { option: 'marque', ...ACCUEIL } }
export const MarqueTelephone: Story = { name: 'Motif de l’identité, téléphone', parameters: { option: 'marque' }, globals: TELEPHONE }
export const MarqueIntrouvable: Story = {
  name: 'Motif de l’identité, page introuvable',
  parameters: { option: 'marque', ...INTROUVABLE },
}
