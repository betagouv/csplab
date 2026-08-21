import type { OrganismesList } from '../types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

const ORGANISME: OrganismesList = {
  organisme_uuid: '11111111-1111-1111-1111-111111111111',
  nom: 'Organisme 1',
  siret: '11004601800021',
  versant: 'FPT',
  gestionnaire: null,
  gestion_ats: false,
  date_derniere_activite: '2026-08-01T00:00:00Z',
  date_creation: '2026-01-01T00:00:00Z',
  nombre_agents: 10,
  nombre_offres_publiees: 5,
}

function mountDrawer(organisme: OrganismesList | null = null) {
  return mount(OrganismeFormDrawer, {
    props: {
      open: true,
      organisme,
    },
    attachTo: document.body,
  })
}

function submitButton() {
  return document.querySelector<HTMLButtonElement>('button[type="submit"]')!
}

async function fill(selector: string, value: string) {
  const input = document.querySelector<HTMLInputElement>(selector)!
  input.value = value
  input.dispatchEvent(new Event('input'))
  await nextTick()
}

async function pickVersant(value: string) {
  const radio = document.querySelector<HTMLElement>(`button[value="${value}"], [role="radio"][value="${value}"]`)
  radio?.click()
  await nextTick()
}

describe('organismeFormDrawer', () => {
  it('keeps the submit button disabled until required fields are filled', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    expect(submitButton().disabled).toBe(true)

    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '12345678901234')
    expect(submitButton().disabled).toBe(true)

    await pickVersant('FPE')
    expect(submitButton().disabled).toBe(false)
    wrapper.unmount()
  })

  it('keeps submit disabled for a malformed siret without showing an error', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '123')
    await pickVersant('FPE')
    expect(submitButton().disabled).toBe(true)
    wrapper.unmount()
  })

  it('emits the payload on create', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '11004601800021')
    await pickVersant('FPT')
    submitButton().click()
    await nextTick()

    const emitted = wrapper.emitted('create')
    expect(emitted).toHaveLength(1)
    expect(emitted![0][0]).toEqual({
      nom: 'Nouvel organisme',
      siret: '11004601800021',
      versant: 'FPT',
      gestion_ats: true,
    })
    wrapper.unmount()
  })

  it('rejects an invalid checksum on submit without emitting', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '12345671234567')
    await pickVersant('FPT')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('create')).toBeUndefined()
    expect(document.body.textContent).toContain(
      'Ce SIRET n\'est pas valide, vérifiez votre saisie.',
    )
    wrapper.unmount()
  })

  it('prefills the form and locks the siret in edition', async () => {
    const wrapper = mountDrawer(ORGANISME)
    await nextTick()

    const siret = document.querySelector<HTMLInputElement>('input[name="siret"]')!
    expect(siret.value).toBe(ORGANISME.siret)
    expect(siret.disabled).toBe(true)
    expect(document.querySelector<HTMLInputElement>('input[name="nom"]')!.value).toBe(ORGANISME.nom)
    expect(document.body.textContent).toContain('Modifier l\'organisme')
    wrapper.unmount()
  })

  it('emits the payload without the siret on update', async () => {
    const wrapper = mountDrawer(ORGANISME)
    await nextTick()
    await fill('input[name="nom"]', 'Organisme renommé')
    submitButton().click()
    await nextTick()

    const emitted = wrapper.emitted('update')
    expect(emitted).toHaveLength(1)
    expect(emitted![0][0]).toEqual({
      nom: 'Organisme renommé',
      versant: 'FPT',
      gestion_ats: false,
    })
    wrapper.unmount()
  })

  it('surfaces a siret conflict on the siret field', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    wrapper.vm.setSiretError('Ce SIRET est déjà utilisé par un autre organisme')
    await nextTick()
    expect(document.body.textContent).toContain('Ce SIRET est déjà utilisé')
    wrapper.unmount()
  })
})
