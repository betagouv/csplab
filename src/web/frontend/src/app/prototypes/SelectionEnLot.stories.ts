import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { expect, userEvent, within } from 'storybook/test'
import { DEMO_CANDIDATURE, DEMO_ORGANISME, DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import App from '@/app/App.vue'

const ORGANISME_PATH = `/organismes/${DEMO_ORGANISME.uuid}`
const RECRUTEMENT_PATH = `${ORGANISME_PATH}/recrutements/${DEMO_RECRUTEMENT_UUID}`
const NOUVEAU_MESSAGE_PATH = `${RECRUTEMENT_PATH}/candidatures/${DEMO_CANDIDATURE.uuid}/messages/nouveau`

const RECEPTION = 'Sélectionner la colonne Candidatures reçues'
const RECRUTEMENTS_SELECTIONNES = ['Gestionnaire de paie', 'Chef de projet systèmes d\'information', 'Inspecteur des installations classées']

const meta = {
  title: 'Prototypes/Sélection en lot',
  component: App,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Vues de l’application rendues par leurs routes, avec les données de démonstration des dossiers `__mocks__`. Le script de chaque story fait la sélection et ouvre le panneau d’action.',
      },
    },
  },
} satisfies Meta<typeof App>

export default meta

type Story = StoryObj<typeof meta>

type Canvas = ReturnType<typeof within>

async function selectReceptionColumn(canvas: Canvas) {
  // CspCheckbox exposes both its reka button and its hidden native input as checkboxes.
  const [checkbox] = await canvas.findAllByRole('checkbox', { name: RECEPTION }, { timeout: 5000 })
  await userEvent.click(checkbox!)
}

async function selectRecrutements(canvas: Canvas) {
  for (const intitule of RECRUTEMENTS_SELECTIONNES) {
    const [checkbox] = await canvas.findAllByRole('checkbox', { name: `Sélectionner ${intitule}` }, { timeout: 5000 })
    await userEvent.click(checkbox!)
  }
}

export const Kanban: Story = {
  parameters: { appRoute: RECRUTEMENT_PATH },
}

export const KanbanColumnSelected: Story = {
  name: 'Kanban, colonne sélectionnée',
  parameters: { appRoute: RECRUTEMENT_PATH },
  play: async ({ canvasElement }) => {
    await selectReceptionColumn(within(canvasElement))
  },
}

export const KanbanCardExcluded: Story = {
  name: 'Kanban, candidature écartée de la sélection',
  parameters: { appRoute: RECRUTEMENT_PATH },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await selectReceptionColumn(canvas)
    const [card] = await canvas.findAllByRole('checkbox', { name: 'Sélectionner Thomas Leroy' })
    await userEvent.click(card!)
  },
}

export const ChangerEtape: Story = {
  name: 'Kanban, panneau Changer d’étape',
  parameters: { appRoute: RECRUTEMENT_PATH },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await selectReceptionColumn(canvas)
    await userEvent.click(await canvas.findByRole('button', { name: 'Changer d\'étape' }))
    await expect(await within(document.body).findByRole('dialog')).toBeVisible()
  },
}

export const Recrutements: Story = {
  name: 'Recrutements, sélection',
  parameters: { appRoute: `${ORGANISME_PATH}/recrutements` },
  play: async ({ canvasElement }) => {
    await selectRecrutements(within(canvasElement))
  },
}

export const AssignerResponsable: Story = {
  name: 'Recrutements, panneau Assigner un responsable',
  parameters: { appRoute: `${ORGANISME_PATH}/recrutements` },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    await selectRecrutements(canvas)
    await userEvent.click(await canvas.findByRole('button', { name: 'Assigner un responsable' }))
    await expect(await within(document.body).findByRole('dialog')).toBeVisible()
  },
}

export const PiecesJointes: Story = {
  name: 'Message, pièces jointes',
  parameters: { appRoute: NOUVEAU_MESSAGE_PATH },
  play: async ({ canvasElement }) => {
    // The candidature panel is a drawer rendered in a portal, outside the story root.
    const page = canvasElement.ownerDocument.body
    await userEvent.type(await within(page).findByLabelText(/Sujet de la conversation/, {}, { timeout: 5000 }), 'Calendrier des entretiens')
    const input = within(page).getByLabelText('Écrivez votre message')
    await userEvent.type(input, 'Bonjour Madame Fontaine,\n\nVous trouverez ci-joint la fiche de poste et le calendrier des entretiens.')
    const fileInput = page.querySelector<HTMLInputElement>('input[type="file"]')!
    await userEvent.upload(fileInput, [
      new File([new Uint8Array(182_000)], 'Fiche_de_poste_gestionnaire_RH.pdf', { type: 'application/pdf' }),
      new File([new Uint8Array(64_000)], 'Calendrier_des_entretiens.pdf', { type: 'application/pdf' }),
      new File([new Uint8Array(41_000)], 'Plan_d_acces.png', { type: 'image/png' }),
    ])
  },
}
