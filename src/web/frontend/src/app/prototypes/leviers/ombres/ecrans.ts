import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { userEvent, within } from 'storybook/test'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'
import { keepTheme } from '../../keepTheme'
import { withLevierOption } from '../options'
import OmbresEtats from './OmbresEtats.vue'
import { OMBRES } from './pistes'

type Story = StoryObj<Meta>

export const RECRUTEMENT_PATH = `/organismes/${DEMO_ORGANISME.uuid}/recrutements/${DEMO_RECRUTEMENT_UUID}`
// The panel opens on its Notes tab: a sandboxed frame, such as a deck slide, blocks the PDF viewer of the CV
const PANNEAU_PATH = `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}/notes`

const page = within(document.body)

// A layer moves the focus into itself when it opens: the screen shows it at rest, without the focus ring
function retirerFocus(): void {
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur()
  }
}

// Opens the popover of the panel that changes the step of the candidature, a layer over the panel
async function ouvrirChangerEtape(): Promise<void> {
  await userEvent.click(await page.findByRole('button', { name: 'Changer d\'étape' }, { timeout: 15000 }))
  await page.findByRole('radio', { name: 'Non retenue' })
  retirerFocus()
}

// Opens the menu of the job offer, under its button at the end of the page header
async function ouvrirMenuDeLOffre(): Promise<void> {
  await userEvent.click(await page.findByRole('button', { name: 'Actions sur l’offre' }, { timeout: 15000 }))
  await page.findByRole('menuitem', { name: 'Personnaliser les étapes de recrutement' })
}

// Moves the candidature to the refusal step, which opens the dialog that asks for the reason
async function ouvrirRefus(): Promise<void> {
  await ouvrirChangerEtape()
  await userEvent.click(await page.findByRole('radio', { name: 'Non retenue' }))
  await userEvent.click(await page.findByRole('button', { name: 'Valider' }))
  await page.findByRole('dialog', { name: 'Refus de candidature' }, { timeout: 15000 })
  retirerFocus()
}

// Meta shared by the stories of the shadow options; each file names its option by parameters.option
export const OMBRES_META = {
  decorators: [keepTheme, withLevierOption(OMBRES)],
  parameters: { layout: 'fullscreen', appRoute: RECRUTEMENT_PATH },
  globals: { interfaceTheme: 'kit' },
  render: () => ({ components: { App }, template: '<App />' }),
} satisfies Meta

const SOMBRE = { theme: 'dark' }
const etats: Story = { render: () => ({ components: { OmbresEtats }, template: '<OmbresEtats />' }) }
const panneau: Story = { parameters: { appRoute: PANNEAU_PATH }, play: ouvrirChangerEtape }

export const ECRANS = {
  etats: { ...etats, name: 'États de la carte' },
  etatsSombre: { ...etats, name: 'États de la carte, sombre', globals: SOMBRE },
  kanban: { name: 'Kanban' },
  menu: { name: 'Menu de l’offre', play: ouvrirMenuDeLOffre },
  panneau: { ...panneau, name: 'Panneau et choix de l’étape' },
  panneauSombre: { ...panneau, name: 'Panneau et choix de l’étape, sombre', globals: SOMBRE },
  dialogue: { name: 'Dialogue du motif de refus', parameters: { appRoute: PANNEAU_PATH }, play: ouvrirRefus },
  etapes: { name: 'Étapes du recrutement', parameters: { appRoute: `${RECRUTEMENT_PATH}/etapes-recrutement` } },
} satisfies Record<string, Story>
