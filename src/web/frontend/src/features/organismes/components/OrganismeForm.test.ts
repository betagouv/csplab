import type { CreateOrganismePayload, UpdateOrganismePayload } from '../types'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { ORGANISME } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import OrganismeForm from './OrganismeForm.vue'

function renderForm(props: Record<string, unknown> = {}) {
  return render(OrganismeForm, { props: { organisme: null, ...props } })
}

function submitButton() {
  return screen.getByRole('button', { name: /Créer l'organisme|Enregistrer les modifications/ })
}

async function fillForm(user: ReturnType<typeof setupUser>, { nom = 'Nouvel organisme', siret = '', versant = '' } = {}) {
  await user.type(await screen.findByRole('textbox', { name: 'Nom de l\'organisme' }), nom)
  if (siret) {
    await user.type(screen.getByRole('textbox', { name: 'SIRET de l\'organisme' }), siret)
  }
  if (versant) {
    await user.click(screen.getByRole('radio', { name: versant }))
  }
}

describe('organismeForm', () => {
  it('keeps the submit button disabled until required fields are filled', async () => {
    const user = setupUser()
    renderForm()

    expect(submitButton()).toBeDisabled()

    await fillForm(user, { siret: '123' })
    expect(submitButton()).toBeDisabled()

    await user.click(screen.getByRole('radio', { name: 'Fonction Publique d\'État' }))
    expect(submitButton()).toBeEnabled()
  })

  it.each([
    ['123', 'Le SIRET doit comporter 14 chiffres.'],
    ['12345671234567', 'Ce SIRET n\'est pas valide, vérifiez votre saisie.'],
  ])('refuses the siret %s on submit', async (siret, message) => {
    const user = setupUser()
    const { emitted } = renderForm()

    await fillForm(user, { siret, versant: 'Fonction Publique d\'État' })
    await user.click(submitButton())

    expect(emitted('create')).toBeUndefined()
    expect(screen.getByText(message)).toBeInTheDocument()
  })

  it('strips non digit characters from a pasted siret', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    await fillForm(user, { siret: '110 046 018 00021', versant: 'Fonction Publique Territoriale' })
    await user.click(submitButton())

    expect(emitted<[CreateOrganismePayload]>('create')[0][0].siret).toBe('11004601800021')
  })

  it('emits the payload on create', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    await fillForm(user, { siret: '11004601800021', versant: 'Fonction Publique Territoriale' })
    await user.click(submitButton())

    expect(emitted<[CreateOrganismePayload]>('create')[0][0]).toEqual({
      nom: 'Nouvel organisme',
      siret: '11004601800021',
      versant: 'FPT',
      gestion_ats: true,
    })
  })

  it('prefills the form and locks the siret in edition', async () => {
    renderForm({ organisme: ORGANISME })

    const siret = screen.getByRole('textbox', { name: 'SIRET de l\'organisme' })
    expect(siret).toHaveValue(ORGANISME.siret)
    expect(siret).toBeDisabled()
    expect(screen.getByRole('textbox', { name: 'Nom de l\'organisme' })).toHaveValue(ORGANISME.nom)
  })

  it('emits the payload without the siret on update', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ organisme: ORGANISME })

    const nom = await screen.findByRole('textbox', { name: 'Nom de l\'organisme' })
    await user.clear(nom)
    await user.type(nom, 'Organisme renommé')
    await user.click(submitButton())

    expect(emitted<[UpdateOrganismePayload]>('update')[0][0]).toEqual({
      nom: 'Organisme renommé',
      versant: 'FPT',
      gestion_ats: false,
    })
  })

  it('surfaces the siret refused by the server until it changes', async () => {
    const user = setupUser()
    renderForm({ rejectedSiret: '11004601800021' })

    await fillForm(user, { siret: '11004601800021' })
    expect(screen.getByText('Ce SIRET est déjà utilisé ou n\'est pas valide.')).toBeInTheDocument()

    await user.type(screen.getByRole('textbox', { name: 'SIRET de l\'organisme' }), '{Backspace}')
    expect(screen.queryByText('Ce SIRET est déjà utilisé ou n\'est pas valide.')).not.toBeInTheDocument()
  })
})
