import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import { SiretConflictError } from '../api'
import OrganismeFormDrawer from './OrganismeFormDrawer.vue'

function mountDrawer() {
  return mount(OrganismeFormDrawer, {
    props: {
      open: true,
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

  it('surfaces a siret conflict on the siret field', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    wrapper.vm.setSiretConflict(new SiretConflictError())
    await nextTick()
    expect(document.body.textContent).toContain('Ce SIRET est déjà utilisé')
    wrapper.unmount()
  })
})
