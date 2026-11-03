import type { StoryObj } from '@storybook/vue3-vite'
import { ref } from 'vue'
import CspFileList from '@/components/base/CspFileList/CspFileList.vue'

const meta = {
  title: 'Éléments/Génériques/CspFileList',
  component: CspFileList,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Liste de fichiers prêts à envoyer : icône, nom, poids et bouton « Retirer » par ligne, avec le message d\'erreur d\'un fichier refusé. La liste est une région `aria-live="polite"` : les lecteurs d\'écran annoncent les fichiers ajoutés et leurs erreurs. Après un retrait, le focus passe au bouton de la ligne suivante, ou de la précédente ; quand la liste se vide, la vue replace le focus, par exemple sur le bouton d\'ajout.',
      },
    },
    controls: { disable: true },
  },
  args: {
    label: 'Fichiers',
    items: [],
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  name: 'Par défaut',
  render: () => ({
    components: { CspFileList },
    setup() {
      const items = ref([
        { key: 'a', name: 'document-a.pdf', size: 820_000 },
        { key: 'b', name: 'document-b.pdf', size: 310_000 },
        { key: 'c', name: 'image-trop-lourde.jpg', size: 12_400_000, error: 'Le fichier dépasse 10 Mo.' },
      ])
      const remove = (key: string) => {
        items.value = items.value.filter(item => item.key !== key)
      }
      return { items, remove }
    },
    template: `<CspFileList label="Fichiers" :items="items" @remove="remove" />`,
  }),
}
