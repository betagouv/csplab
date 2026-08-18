import type { OrganismeAdmin } from '../types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import { SiretConflictError } from '../api'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

const ORGANISME: OrganismeAdmin = {
  uuid: '11111111-1111-1111-1111-111111111111',
  nom: 'Organisme 1',
  siret: '11111111111111',
  versant: 'FPT',
  gestion_candidatures: false,
  gestionnaire: null,
}

function mountDrawer(props: { organisme?: OrganismeAdmin | null } = {}) {
  return mount(OrganismeFormDrawer, {
    props: {
      open: true,
      organisme: props.organisme ?? null,
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

describe('organismeFormDrawer', () => {
  it('keeps the submit button disabled until required fields are filled', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    expect(submitButton().disabled).toBe(true)

    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '12345678901234')
    expect(submitButton().disabled).toBe(true)

    const versant = document.querySelector<HTMLElement>('button[value="FPE"], [role="radio"][value="FPE"]')
    versant?.click()
    await nextTick()
    expect(submitButton().disabled).toBe(false)
    wrapper.unmount()
  })

  it('keeps submit disabled for a malformed siret without showing an error', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '123')
    expect(submitButton().disabled).toBe(true)
    expect(document.body.textContent).not.toContain('SIRET doit')
    wrapper.unmount()
  })

  it('prefills and disables the siret in edition mode', async () => {
    const wrapper = mountDrawer({ organisme: ORGANISME })
    await nextTick()
    const siret = document.querySelector<HTMLInputElement>('input[name="siret"]')!
    expect(siret.value).toBe(ORGANISME.siret)
    expect(siret.disabled).toBe(true)
    expect(document.body.textContent).toContain('Modifier l\'organisme')
    expect(document.body.textContent).toContain('Enregistrer les modifications')
    wrapper.unmount()
  })

  it('emits the payload on submit', async () => {
    const wrapper = mountDrawer({ organisme: ORGANISME })
    await nextTick()
    await fill('input[name="nom"]', 'Organisme renommé')
    submitButton().click()
    await nextTick()

    const emitted = wrapper.emitted('submit')
    expect(emitted).toHaveLength(1)
    expect(emitted![0][0]).toEqual({
      nom: 'Organisme renommé',
      siret: ORGANISME.siret,
      versant: 'FPT',
      gestion_candidatures: false,
    })
    wrapper.unmount()
  })

  it('surfaces a siret conflict on the siret field', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    wrapper.vm.setSiretConflict(new SiretConflictError())
    await nextTick()
    expect(document.body.textContent).toContain('Ce SIRET est déjà utilisé')
    wrapper.unmount()
  })
})
