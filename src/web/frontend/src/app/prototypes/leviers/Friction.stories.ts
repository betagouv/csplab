import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { keepTheme } from '../keepTheme'
import FrictionPlanche from './FrictionPlanche.vue'

const meta = {
  title: 'Prototypes/Leviers/Actions destructrices',
  component: FrictionPlanche,
  decorators: [keepTheme],
  parameters: { layout: 'fullscreen' },
  globals: { interfaceTheme: 'aucun' },
} satisfies Meta<typeof FrictionPlanche>

export default meta

type Story = StoryObj<typeof meta>

export const EtapeKit: Story = { name: 'Supprimer une étape, kit actuel', args: { cas: 'etape' } }
export const EtiquetteAnnuler: Story = { name: 'Retirer une étiquette, annulation', args: { cas: 'etiquette' } }
export const EquipeConfirmation: Story = { name: 'Retirer un membre de l’équipe, confirmation', args: { cas: 'equipe' } }
export const EtapeSaisie: Story = { name: 'Supprimer une étape, saisie du nom', args: { cas: 'etape-saisie' } }

export const DegreNeutre: Story = { name: 'Degré 1, bleu France', args: { cas: 'etape-saisie', degre: 'neutre', nomSaisi: true } }
export const DegrePicto: Story = { name: 'Degré 2, pictogramme', args: { cas: 'etape-saisie', degre: 'picto', nomSaisi: true } }
export const DegreContourRouge: Story = { name: 'Degré 3, contour rouge', args: { cas: 'etape-saisie', degre: 'contour-rouge', nomSaisi: true } }
export const DegrePleinRouge: Story = { name: 'Degré 4, rouge plein et alerte', args: { cas: 'etape-saisie', degre: 'plein-rouge', nomSaisi: true } }
