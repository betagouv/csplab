import type { Meta, StoryObj } from '@storybook/vue3-vite'
import type { FondSurfaceDessinee } from './planche'
import { DEMO_ORGANISME } from '@/api/__mocks__/demo'
import { keepTheme } from '../../keepTheme'
import { PLANCHE_DEGRADE } from './degrade'
import { SOMBRE } from './ecrans'
import { PLANCHE_GREIGE } from './greige'
import { EN_TETE_DISCRET, PLANCHE_MARQUE } from './marque'
import { ETAT_VIDE_DISCRET, PLANCHE_PICTOGRAMMES } from './pictogrammes'
import PistesPlanche from './PistesPlanche.vue'

const meta = {
  title: 'Prototypes/Leviers/Fonds/Comparaison',
  decorators: [keepTheme],
  // The breadcrumb of the page header links through the router of the application
  parameters: { layout: 'fullscreen', appRoute: `/organismes/${DEMO_ORGANISME.uuid}` },
  globals: { interfaceTheme: 'kit' },
} satisfies Meta

export default meta

type Story = StoryObj<typeof meta>

// The page header in the variant that each track gives the working screens, and the empty state in the discrete
// variant in each track
const EN_TETES = [
  { nom: 'Dégradés et textures', surface: PLANCHE_DEGRADE.page },
  { nom: 'Motif de l’identité de csplab', surface: EN_TETE_DISCRET },
  { nom: 'Pictogrammes du DSFR', surface: PLANCHE_PICTOGRAMMES.page },
  { nom: 'Greige', surface: PLANCHE_GREIGE.page },
]

const ETATS_VIDES = [
  { nom: 'Dégradés et textures', surface: PLANCHE_DEGRADE.etatVide },
  { nom: 'Motif de l’identité de csplab', surface: PLANCHE_MARQUE.etatVide },
  { nom: 'Pictogrammes du DSFR', surface: ETAT_VIDE_DISCRET },
  { nom: 'Greige', surface: PLANCHE_GREIGE.etatVide },
]

function planche(surface: 'en-tete' | 'etat-vide', titre: string, pistes: { nom: string, surface: FondSurfaceDessinee }[]): Story {
  return {
    render: () => ({
      components: { PistesPlanche },
      setup: () => ({ surface, titre, pistes }),
      template: '<PistesPlanche :surface="surface" :titre="titre" :pistes="pistes" />',
    }),
  }
}

const enTete = planche('en-tete', 'En-tête de page des écrans de travail', EN_TETES)
const etatVide = planche('etat-vide', 'État vide', ETATS_VIDES)

export const EnTete: Story = { ...enTete, name: 'En-tête de page' }
export const EnTeteSombre: Story = { ...enTete, name: 'En-tête de page, sombre', globals: SOMBRE }
export const EtatVide: Story = { ...etatVide, name: 'État vide' }
export const EtatVideSombre: Story = { ...etatVide, name: 'État vide, sombre', globals: SOMBRE }
