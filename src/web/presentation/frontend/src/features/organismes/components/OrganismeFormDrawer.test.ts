import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
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

  it('emits the payload on submit', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fill('input[name="nom"]', 'Nouvel organisme')
    await fill('input[name="siret"]', '11004601800021')
    await pickVersant('FPT')
    submitButton().click()
    await nextTick()

    const emitted = wrapper.emitted('submit')
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

    expect(wrapper.emitted('submit')).toBeUndefined()
    expect(document.body.textContent).toContain(
      'Ce SIRET n\'est pas valide, vérifiez votre saisie.',
    )
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
