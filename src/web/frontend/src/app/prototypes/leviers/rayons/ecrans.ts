import type { Decorator, Meta, StoryObj } from '@storybook/vue3-vite'
import type { LevierOption } from '../options'
import { onBeforeUnmount } from 'vue'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import CspSkeletonSortableList from '@/components/base/CspSkeleton/CspSkeletonSortableList.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import { useToast } from '@/composables/ui/useToast'
import { keepTheme } from '../../keepTheme'
import LeviersDetail from '../LeviersDetail.vue'
import { withLevierOption } from '../options'
import ImbricationsPlanche from './ImbricationsPlanche.vue'

type Story = StoryObj<Meta>

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
export const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`
const PANNEAU_PATH = `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}`

// Meta shared by the story files of the radius tracks, which write the option named by parameters.option
export function rayonsMeta(options: LevierOption[]) {
  return {
    decorators: [keepTheme, withLevierOption(options)],
    parameters: {
      layout: 'fullscreen',
      appRoute: RECRUTEMENT_PATH,
      viewport: {
        options: { telephone: { name: 'Téléphone, 375 px', styles: { width: '375px', height: '812px' }, type: 'mobile' } },
      },
    },
    globals: { interfaceTheme: 'kit' },
    render: () => ({ components: { App }, template: '<App />' }),
  } satisfies Meta
}

// The element that the application shows once it has loaded the demo data
async function attendre<E extends HTMLElement>(trouver: () => E | null | undefined): Promise<E> {
  for (let essai = 0; essai < 100; essai++) {
    const element = trouver()
    if (element) {
      return element
    }
    await new Promise(resolve => setTimeout(resolve, 100))
  }
  throw new Error('Élément introuvable')
}

// Clicks a button that opens a dialog, once the application has enabled it
function ouvrir(libelle: string): Pick<Story, 'play'> {
  return {
    play: async () => {
      const bouton = await attendre(() => [...document.querySelectorAll<HTMLButtonElement>('button')]
        .find(element => element.textContent?.trim() === libelle && !element.disabled))
      bouton.click()
    },
  }
}

// Opened from the keyboard, the menu of the job offer highlights its first item
const menu: Pick<Story, 'play'> = {
  play: async () => {
    const declencheur = await attendre(() => document.querySelector<HTMLElement>('[aria-label="Actions sur l’offre"]'))
    declencheur.focus()
    declencheur.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }))
  },
}

// A notification with an action, as the kanban shows it after a change of step, kept on screen
const avecNotification: Decorator = story => ({
  components: { story },
  setup() {
    const { addToast, dismissToast } = useToast()
    const id = addToast({
      variant: 'success',
      title: 'Étape modifiée',
      description: 'Clara Fontaine est passée à l’étape Entretien.',
      duration: 1e9,
      action: { label: 'Annuler', onSelect: () => {} },
    })
    onBeforeUnmount(() => dismissToast(id))
  },
  template: '<story />',
})

// The screens that each track shows, as parameters, globals, play, decorators or render of a story
export const PANNEAU = { appRoute: PANNEAU_PATH }
export const NOTES = { appRoute: `${PANNEAU_PATH}/notes` }
export const DOCUMENTS = { appRoute: `${PANNEAU_PATH}/documents` }
export const MESSAGES = { appRoute: `${PANNEAU_PATH}/messages` }
export const LISTE = { appRoute: `${RECRUTEMENT_PATH}/liste` }
export const PARAMETRES = { appRoute: ORGANISME_PATH }
export const ETAPES = { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` }
export const TELEPHONE = { viewport: { value: 'telephone', isRotated: false } }
export const SOMBRE = { theme: 'dark' }
export const DIALOGUE = ouvrir('Ajouter une étape')
export const CONFIRMATION = ouvrir('Réinitialiser')
export const MENU = menu
export const NOTIFICATION = { decorators: [avecNotification] }
export const COMPOSANTS = {
  render: () => ({ components: { LeviersDetail }, template: '<LeviersDetail variante="arrondis" />' }),
}
export const IMBRICATIONS = { render: () => ({ components: { ImbricationsPlanche }, template: '<ImbricationsPlanche />' }) }
// Loading placeholders of the kanban, of the steps list and of a table
export const CHARGEMENT = {
  render: () => ({
    components: { CspSkeletonKanban, CspSkeletonSortableList, CspSkeletonTable },
    template: `<div style="display: grid; gap: var(--csp-space-8); padding: var(--csp-space-8)">
      <CspSkeletonKanban :columns="4" :cards="2" />
      <div style="display: grid; grid-template-columns: 38rem 1fr; gap: var(--csp-space-8); align-items: start">
        <CspSkeletonSortableList :rows="4" />
        <CspSkeletonTable :rows="4" />
      </div>
    </div>`,
  }),
}
