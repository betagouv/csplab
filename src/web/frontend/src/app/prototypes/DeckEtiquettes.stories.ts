import type { Decorator, Meta, StoryObj } from '@storybook/vue3-vite'
import { onBeforeUnmount } from 'vue'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import DeckEtiquettes from './DeckEtiquettes.vue'

// A deck loads several of these stories at once, and the application reads its color mode from the localStorage they share:
// the decorator puts the theme of the story back when the application changes it.
const keepTheme: Decorator = (story, context) => ({
  components: { story },
  setup() {
    const root = document.documentElement
    const observer = new MutationObserver(() => {
      if (root.getAttribute('data-fr-theme') !== context.globals.theme) {
        root.setAttribute('data-fr-theme', context.globals.theme)
      }
    })
    observer.observe(root, { attributes: true, attributeFilter: ['data-fr-theme'] })
    onBeforeUnmount(() => observer.disconnect())
  },
  template: '<story />',
})

const withBorder: Decorator = story => ({
  components: { story },
  setup() {
    document.documentElement.classList.add('deck-filet')
    onBeforeUnmount(() => document.documentElement.classList.remove('deck-filet'))
  },
  template: '<story />',
})

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

const CANDIDATURE_ROUTE = { appRoute: `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}/candidatures/${DEMO_CANDIDATURE.uuid}` }

const ECRAN: Story = {
  args: { planche: 'cartes' },
  render: () => ({ components: { App }, template: '<App />' }),
  parameters: CANDIDATURE_ROUTE,
}

export const Ecran: Story = {
  ...ECRAN,
  name: 'Kanban et panneau de candidature',
  globals: DSFR,
}

export const EcranKitLight: Story = {
  ...ECRAN,
  name: 'Kanban et panneau de candidature, palette du kit, thème clair',
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const EcranKitDark: Story = {
  ...ECRAN,
  name: 'Kanban et panneau de candidature, palette du kit, thème sombre',
  globals: { etiquettes: 'kit', theme: 'dark' },
}

export const EcranKitFiletLight: Story = {
  ...ECRAN,
  name: 'Kanban et panneau de candidature, palette du kit avec filet, thème clair',
  decorators: [withBorder],
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const EcranKitFiletDark: Story = {
  ...ECRAN,
  name: 'Kanban et panneau de candidature, palette du kit avec filet, thème sombre',
  decorators: [withBorder],
  globals: { etiquettes: 'kit', theme: 'dark' },
}

export const TagDsfr: Story = {
  name: 'Tag du DSFR',
  args: { planche: 'tag-dsfr' },
  globals: DSFR,
}

export const BadgeDsfr: Story = {
  name: 'Badge du DSFR',
  args: { planche: 'badge-dsfr' },
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
  parameters: CANDIDATURE_ROUTE,
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
  parameters: CANDIDATURE_ROUTE,
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

export const FiletContexteLight: Story = {
  name: 'Filet sur fond gris, thème clair',
  args: { planche: 'filet-contexte' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const FiletContexteDark: Story = {
  name: 'Filet sur fond gris, thème sombre',
  args: { planche: 'filet-contexte' },
  globals: { etiquettes: 'kit', theme: 'dark' },
}

export const RondeLight: Story = {
  name: 'Étiquette ronde, thème clair',
  args: { planche: 'ronde' },
  globals: { etiquettes: 'kit', theme: 'light' },
}

export const RondeDark: Story = {
  name: 'Étiquette ronde, thème sombre',
  args: { planche: 'ronde' },
  globals: { etiquettes: 'kit', theme: 'dark' },
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
