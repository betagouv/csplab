import type { ComponentPropsAndSlots, StoryObj } from '@storybook/vue3-vite'
import CspAccordion from '@/components/base/CspAccordion/CspAccordion.vue'
import CspAccordionItem from '@/components/base/CspAccordion/CspAccordionItem.vue'

type CspAccordionProps = ComponentPropsAndSlots<typeof CspAccordion>

const ITEMS = [
  { value: 'item-1', title: 'Première question', content: 'Réponse à la première question.' },
  { value: 'item-2', title: 'Deuxième question', content: 'Réponse à la deuxième question.' },
  { value: 'item-3', title: 'Troisième question', content: 'Réponse à la troisième question.' },
]

const meta = {
  title: 'Éléments/Génériques/CspAccordion',
  component: CspAccordion,
  tags: ['autodocs'],
  parameters: {
    controls: {
      include: ['type', 'collapsible', 'defaultValue'],
    },
    docs: {
      description: {
        component: 'Accordéon accessible basé sur Reka UI. Placez un `CspAccordionItem` (`value`, `title`, contenu en slot) par section dépliable. Chaque titre est un bouton dans un `<h3>` par défaut (prop `headingLevel` du `CspAccordionItem` pour l\'ajuster au plan de la page), avec `aria-expanded` et `aria-controls` ; les flèches, Début et Fin passent d\'un titre à l\'autre au sein d\'un même accordéon.',
      },
    },
  },
  argTypes: {
    type: {
      control: { type: 'radio' },
      options: ['single', 'multiple'],
      description: 'Une seule section ouverte à la fois, ou plusieurs.',
      table: {
        type: { summary: '\'single\' | \'multiple\'' },
        defaultValue: { summary: '\'multiple\'' },
      },
    },
    collapsible: {
      control: { type: 'boolean' },
      description: 'En mode `single`, permet de refermer la section ouverte.',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'true' },
      },
    },
    defaultValue: {
      control: { type: 'object' },
      description: 'Section(s) ouverte(s) au premier rendu.',
      table: {
        type: { summary: 'string | string[]' },
      },
    },
  },
  args: {
    type: 'multiple',
    collapsible: true,
  },
  render: (args: CspAccordionProps) => ({
    components: { CspAccordion, CspAccordionItem },
    setup() {
      return { args, items: ITEMS }
    },
    template: `
      <CspAccordion v-bind="args">
        <CspAccordionItem
          v-for="item in items"
          :key="item.value"
          :value="item.value"
          :title="item.title"
        >
          <p>{{ item.content }}</p>
        </CspAccordionItem>
      </CspAccordion>
    `,
  }),
}

export default meta
type Story = StoryObj<CspAccordionProps>

export const Default: Story = {
  name: 'Par défaut',
}

export const OuvertParDefaut: Story = {
  name: 'Ouvert par défaut',
  args: {
    defaultValue: ['item-1'],
  },
}

export const Single: Story = {
  name: 'Une section à la fois',
  args: {
    type: 'single',
    defaultValue: 'item-1',
  },
}

export const PlusieursOuvertes: Story = {
  name: 'Plusieurs sections ouvertes',
  args: {
    type: 'multiple',
    defaultValue: ['item-1', 'item-3'],
  },
}

const LONG_CONTENT = 'Une réponse longue, découpée en paragraphes et en liste, pour vérifier le retour à la ligne et l\'espacement.\n- Premier point de la liste, assez long pour passer sur plusieurs lignes lorsque la largeur disponible est réduite.\n- Deuxième point de la liste.\n- Troisième point de la liste.\n\nUn dernier paragraphe conclut la réponse et rappelle où trouver plus d\'informations.'

export const ContenuLong: Story = {
  name: 'Contenu long',
  args: {
    defaultValue: ['item-long'],
  },
  render: (args: CspAccordionProps) => ({
    components: { CspAccordion, CspAccordionItem },
    setup() {
      return { args, content: LONG_CONTENT, items: ITEMS.slice(1) }
    },
    template: `
      <CspAccordion v-bind="args">
        <CspAccordionItem
          value="item-long"
          title="Une question dont la réponse est longue et dont le titre lui-même s'étend sur plusieurs lignes quand la place manque"
        >
          <p style="white-space: pre-line">{{ content }}</p>
        </CspAccordionItem>
        <CspAccordionItem
          v-for="item in items"
          :key="item.value"
          :value="item.value"
          :title="item.title"
        >
          <p>{{ item.content }}</p>
        </CspAccordionItem>
      </CspAccordion>
    `,
  }),
}
