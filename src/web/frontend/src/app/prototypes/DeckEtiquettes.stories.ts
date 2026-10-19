import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import DeckEtiquettes from './DeckEtiquettes.vue'
import { keepTheme } from './keepTheme'

const meta = {
  title: 'Prototypes/Deck étiquettes',
  component: DeckEtiquettes,
  decorators: [keepTheme],
  parameters: {
    layout: 'fullscreen',
    appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`,
  },
} satisfies Meta<typeof DeckEtiquettes>

export default meta

type Story = StoryObj<typeof meta>

const DSFR = { etiquettes: 'repli', theme: 'light' }

export const TagDsfr: Story = {
  name: 'Tag du DSFR',
  args: { planche: 'tag-dsfr' },
  globals: DSFR,
}

export const TagDsfrCouleur: Story = {
  name: 'Tag du DSFR, couleur',
  args: { planche: 'tag-dsfr-couleur' },
  globals: DSFR,
}

export const BadgeDsfr: Story = {
  name: 'Badge du DSFR',
  args: { planche: 'badge-dsfr' },
  globals: DSFR,
}

export const BadgeDsfrCouleurs: Story = {
  name: 'Badge du DSFR, couleurs',
  args: { planche: 'badge-dsfr-couleurs' },
  globals: DSFR,
}

export const CouleursDsfrLight: Story = {
  name: 'Couleurs illustratives du DSFR, thème clair',
  args: { planche: 'couleurs-dsfr' },
  globals: DSFR,
}

export const CouleursDsfrDark: Story = {
  name: 'Couleurs illustratives du DSFR, thème sombre',
  args: { planche: 'couleurs-dsfr' },
  globals: { etiquettes: 'repli', theme: 'dark' },
}

export const HypotheseCartes: Story = {
  name: 'Tag du DSFR, cartes du kanban',
  args: { planche: 'cartes', formeTag: true },
  globals: DSFR,
}

export const HypothesePanneau: Story = {
  name: 'Tag du DSFR, colonne de droite du panneau',
  args: { planche: 'panneau', formeTag: true },
  globals: DSFR,
}

export const LasuiteLight: Story = {
  name: 'Couleurs de La Suite numérique, thème clair',
  args: { planche: 'palette' },
  globals: { etiquettes: 'lasuite', theme: 'light' },
}

export const LasuiteDark: Story = {
  name: 'Couleurs de La Suite numérique, thème sombre',
  args: { planche: 'palette' },
  globals: { etiquettes: 'lasuite', theme: 'dark' },
}

export const KitLight: Story = {
  name: 'Palette du kit, thème clair',
  args: { planche: 'palette' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const KitDark: Story = {
  name: 'Palette du kit, thème sombre',
  args: { planche: 'palette' },
  globals: { etiquettes: 'kit', theme: 'dark' },
}

export const KitContrastes: Story = {
  name: 'Palette du kit, contrastes',
  args: { planche: 'contrastes' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const KitEcarts: Story = {
  name: 'Palette du kit, écarts',
  args: { planche: 'ecarts' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const KitDaltonisme: Story = {
  name: 'Palette du kit, daltonisme simulé',
  args: { planche: 'daltonisme' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BadgeCartes: Story = {
  name: 'Badge métier, cartes du kanban',
  args: { planche: 'cartes' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BadgePanneau: Story = {
  name: 'Badge métier, colonne de droite du panneau',
  args: { planche: 'panneau' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BadgeNote: Story = {
  name: 'Badge métier, note',
  args: { planche: 'note' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BadgeVoisins: Story = {
  name: 'Badge métier, filtre, statuts et bouton',
  args: { planche: 'voisins' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BorduresLight: Story = {
  name: 'Bordures, thème clair',
  args: { planche: 'bordures' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const BorduresDark: Story = {
  name: 'Bordures, thème sombre',
  args: { planche: 'bordures' },
  globals: { etiquettes: 'kit', theme: 'dark' },
}
