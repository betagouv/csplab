import type { ComponentPropsAndSlots, Meta, StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'

type CspSearchBarProps = ComponentPropsAndSlots<typeof CspSearchBar>

const meta = {
  title: 'Éléments/Génériques/CspSearchBar',
  component: CspSearchBar,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['label', 'mode', 'hideLabel', 'hint', 'placeholder', 'size', 'disabled', 'error', 'errorMessage', 'buttonLabel'],
    },
    docs: {
      description: {
        component: 'Barre de recherche DSFR, en deux modes. En mode `submit`, par défaut, la recherche se lance à la validation : un bouton accompagne le champ, et l’événement `search` porte la valeur sans espaces superflus au clic ou à la touche Entrée. En mode `live`, la recherche suit la saisie par le `v-model` : le bouton disparaît et une loupe discrète signale le champ de recherche. La touche Entrée émet toujours `search`, pour appliquer un filtre qui attend une pause dans la frappe. Le libellé peut être masqué visuellement dans une barre d’outils, il reste le nom accessible du champ. Deux tailles : MD pour une recherche contextuelle, LG pour un moteur mis en avant.',
      },
    },
  },
  argTypes: {
    mode: {
      control: 'radio',
      options: ['submit', 'live'],
    },
    size: {
      control: 'radio',
      options: ['md', 'lg'],
    },
  },
  args: {
    label: 'Rechercher',
    placeholder: 'Rechercher',
    size: 'md',
  },
} satisfies Meta<CspSearchBarProps>

export default meta
type Story = StoryObj<CspSearchBarProps>

function render(args: CspSearchBarProps) {
  return {
    components: { CspSearchBar },
    setup() {
      const value = ref('')
      const submitted = ref('')
      return { args, value, submitted }
    },
    template: `
      <div style="max-width: 32rem;">
        <CspSearchBar v-bind="args" v-model="value" @search="submitted = $event" />
        <p v-if="submitted" style="margin-top: 1rem; font-size: 0.875rem; color: var(--text-mention-grey);">Recherche lancée : {{ submitted }}</p>
      </div>
    `,
  }
}

export const Default: Story = {
  render,
}

export const Live: Story = {
  name: 'Filtre au fil de la saisie',
  args: { mode: 'live', hideLabel: true, placeholder: 'Filtrer la liste' },
  render,
}

export const Large: Story = {
  args: { size: 'lg' },
  render,
}

export const HiddenLabel: Story = {
  name: 'Libellé masqué',
  args: { hideLabel: true },
  render,
}

export const WithHint: Story = {
  name: 'Avec indication',
  args: { label: 'Adresse email', hint: 'Adresse complète du compte', placeholder: 'prenom.nom@exemple.gouv.fr' },
  render,
}

export const Error: Story = {
  args: { error: true, errorMessage: 'Aucun résultat pour cette recherche.' },
  render,
}

export const Disabled: Story = {
  args: { disabled: true },
  render,
}
