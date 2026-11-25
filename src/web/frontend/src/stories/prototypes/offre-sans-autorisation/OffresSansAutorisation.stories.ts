import type { StoryObj } from '@storybook/vue3-vite'
import AtsApp from './variants/mvp/AtsApp.vue'

// Création manuelle des offres, parcours SANS autorisation (MVP) : brouillon → publiée → dépubliée.
// D'après le doc « Création manuelle des offres ». Le proto « ATS — fiches de poste et offres » (avec validation)
// reste à côté. Données fictives, conservées pendant la session.
const meta = {
  title: 'Prototypes/Offres sans autorisation (MVP)',
  id: 'prototypes-offre-mvp',
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Organisme sans circuit d\'autorisation. « Créer une offre » ouvre le formulaire vide, « Dupliquer » (menu « … ») '
          + 'le formulaire pré-rempli. Formulaire en 7 étapes, en deux parties : annonce visible du candidat (le poste, le métier, cadre, '
          + 'profil et conditions, employeur et lieux) et paramétrage des candidatures (formulaire, documents). Publier → aperçu candidat '
          + '→ fenêtre de succès (afficher le recrutement ou retourner aux offres). Page de l\'offre en blocs modifiables un par un. '
          + 'Hypothèses : NOTES.md.',
      },
    },
  },
}

export default meta
type Story = StoryObj

function story(depart: Record<string, unknown>, publier = true): Story['render'] {
  return () => ({
    components: { AtsApp },
    setup: () => ({ depart, publier }),
    template: '<AtsApp :depart="depart" :publier="publier" />',
  })
}

export const MesOffres: Story = { name: '1. Mes offres d\'emploi', render: story({ nom: 'offres' }) }
export const Creer: Story = { name: '2. Créer une offre — formulaire vide en étapes', render: story({ nom: 'creation' }) }
export const Rediger: Story = { name: '3. Formulaire en étapes — brouillon à compléter', render: story({ nom: 'rediger', id: 'OFF-2026-0151' }) }
export const Brouillon: Story = { name: '4. Brouillon complet — page de l\'offre en blocs', render: story({ nom: 'offre', id: 'OFF-2026-0145' }) }
export const Publier: Story = { name: '5. Publier — aperçu candidat et validation', render: story({ nom: 'publier', id: 'OFF-2026-0145' }) }
export const Publiee: Story = { name: '6. Offre publiée — modifiable, prolonger ou retirer', render: story({ nom: 'offre', id: 'OFF-2026-0131' }) }
export const FinProche: Story = { name: '6 bis. Offre publiée qui se termine dans 4 jours', render: story({ nom: 'offre', id: 'OFF-2026-0118' }) }
export const Depubliee: Story = { name: '7. Offre dépubliée — prolonger pour la remettre en ligne', render: story({ nom: 'offre', id: 'OFF-2026-0122' }) }
export const Duplication: Story = { name: '8. Brouillon issu d\'une duplication', render: story({ nom: 'offre', id: 'OFF-2026-0156' }) }
export const SansDroitPublier: Story = { name: '9. Agent sans le droit « Publier »', render: story({ nom: 'offre', id: 'OFF-2026-0145' }, false) }
export const Recrutements: Story = { name: '10. Mes recrutements', render: story({ nom: 'recrutements' }) }
export const Parametres: Story = { name: '11. Paramètres — droits Créer et Publier', render: story({ nom: 'parametres' }) }
