import type { Meta } from '@storybook/vue3-vite'
import type { LevierOption } from '../options'
import { DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import { withLevierOption } from '../options'
import EtatsVidesPlanche from './EtatsVidesPlanche.vue'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`
// First candidature of the demo, whose notes and messages are empty
const SANS_NOTE_UUID = 'd0000000-0000-4000-8000-000000000001'

// Meta shared by the story files of the background tracks, which write the option named by parameters.option
export function fondsMeta(options: LevierOption[]) {
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

// The screens that each track shows, as parameters, globals or render of a story. The panel opens on the Notes tab of a
// candidature without notes, which shows an empty state: a sandboxed frame, such as a deck slide, blocks the PDF viewer
// of the CV.
export const PANNEAU = { appRoute: `${RECRUTEMENT_PATH}/candidatures/${SANS_NOTE_UUID}/notes` }
export const PARAMETRES = { appRoute: ORGANISME_PATH }
export const ACCUEIL = { appRoute: '/' }
export const INTROUVABLE = { appRoute: '/page-introuvable' }
export const TELEPHONE = { viewport: { value: 'telephone', isRotated: false } }
export const SOMBRE = { theme: 'dark' }
export const ETATS_VIDES = { render: () => ({ components: { EtatsVidesPlanche }, template: '<EtatsVidesPlanche />' }) }
