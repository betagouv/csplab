import type { Meta, StoryObj } from '@storybook/vue3-vite'
import CspAccordion from '@/components/base/CspAccordion/CspAccordion.vue'
import CspAccordionItem from '@/components/base/CspAccordion/CspAccordionItem.vue'
import { FAQ_ENTREES, FAQ_THEMES } from '../constants/faq'

function entreesTemplate(source: string): string {
  return `
  <CspAccordionItem
    v-for="entree in ${source}"
    :key="entree.id"
    :value="entree.id"
    :title="entree.question"
  >
    <p style="margin: 0 0 0.75rem; white-space: pre-line">{{ entree.reponse }}</p>
    <p style="margin: 0; font-size: 0.875rem; color: var(--text-mention-grey)">
      <strong>Où :</strong> {{ entree.ou }}
    </p>
  </CspAccordionItem>
`
}

const meta = {
  title: 'Compositions/ATS/Aide — FAQ recruteur',
  component: CspAccordion,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
    controls: {
      disable: true,
    },
    docs: {
      description: {
        component: 'FAQ recruteur de la page Aide : CspAccordion composé avec les entrées réelles de la feature (constants/faq.ts), un accordéon par thème, rendu comme dans AideView.',
      },
    },
  },
} satisfies Meta<typeof CspAccordion>

export default meta
type Story = StoryObj<typeof meta>

export const ThemeDemarrer: Story = {
  name: 'Thème Démarrer (première entrée dépliée)',
  render: () => ({
    components: { CspAccordion, CspAccordionItem },
    setup() {
      const entrees = FAQ_ENTREES.filter(entree => entree.theme === 'Démarrer')
      return { entrees, premiere: entrees[0]?.id }
    },
    template: `
      <CspAccordion :default-value="premiere ? [premiere] : undefined">
        ${entreesTemplate('entrees')}
      </CspAccordion>
    `,
  }),
}

export const ToutesLesEntrees: Story = {
  name: 'Toutes les entrées',
  render: () => ({
    components: { CspAccordion, CspAccordionItem },
    setup() {
      const sections = FAQ_THEMES.map((titre, index) => ({
        id: `aide-theme-${index}`,
        titre,
        entrees: FAQ_ENTREES.filter(entree => entree.theme === titre),
      }))
      return { sections }
    },
    template: `
      <section
        v-for="(section, index) in sections"
        :key="section.id"
        :style="index > 0 ? 'margin-top: 2rem' : undefined"
      >
        <h2
          :id="section.id"
          style="margin: 0 0 0.75rem; font-size: 1.25rem; font-weight: 700; color: var(--text-title-grey)"
        >
          {{ section.titre }}
        </h2>
        <CspAccordion>
          ${entreesTemplate('section.entrees')}
        </CspAccordion>
      </section>
    `,
  }),
}
