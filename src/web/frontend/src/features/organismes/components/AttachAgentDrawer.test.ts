import type { AgentRecherche } from '../types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import AttachAgentDrawer from './AttachAgentDrawer.vue'

const AGENT: AgentRecherche = {
  agent_id: 'aaaaaaaa-0001-0001-0001-000000000001',
  email: 'jeanne.dupont@example.gouv.fr',
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Responsable recrutement',
}

function mountDrawer(props: Record<string, unknown> = {}) {
  return mount(AttachAgentDrawer, {
    props: {
      open: true,
      status: 'idle',
      agent: null,
      ...props,
    },
    attachTo: document.body,
  })
}

function submitButton() {
  return document.querySelector<HTMLButtonElement>('button[type="submit"]')!
}

async function fillEmail(value: string) {
  const input = document.querySelector<HTMLInputElement>('input[name="email"]')!
  input.value = value
  input.dispatchEvent(new Event('input'))
  await nextTick()
}

async function pickRole(value: string) {
  const radio = document.querySelector<HTMLElement>(`button[value="${value}"], [role="radio"][value="${value}"]`)
  radio?.click()
  await nextTick()
}

describe('attachAgentDrawer', () => {
  it('rejects an invalid email without emitting a search', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fillEmail('jeanne.dupont')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('search')).toBeUndefined()
    expect(document.body.textContent).toContain('Renseignez une adresse électronique valide.')
    wrapper.unmount()
  })

  it('emits the trimmed email on search', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await fillEmail('  jeanne.dupont@example.gouv.fr  ')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('search')).toEqual([['jeanne.dupont@example.gouv.fr']])
    wrapper.unmount()
  })

  it('shows the matching agent without any editable identity field', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()

    expect(document.body.textContent).toContain('Jeanne Dupont')
    expect(document.body.textContent).toContain('Responsable recrutement')
    expect(document.body.textContent).toContain('jeanne.dupont@example.gouv.fr')
    expect(document.querySelector('input[name="nom"]')).toBeNull()
    expect(document.querySelector('input[name="prenom"]')).toBeNull()
    wrapper.unmount()
  })

  it('attaches the agent as membre by default', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('attach')).toEqual([['membre']])
    wrapper.unmount()
  })

  it('attaches the agent with the selected role', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()
    await pickRole('responsable')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('attach')).toEqual([['responsable']])
    wrapper.unmount()
  })

  it('blocks the submission when no account matches', async () => {
    const wrapper = mountDrawer({ status: 'not-found' })
    await nextTick()

    expect(document.body.textContent).toContain('Aucun compte ne correspond à cette adresse.')
    expect(submitButton().disabled).toBe(true)
    wrapper.unmount()
  })

  it('asks for a reset when the email changes after a search', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()
    await fillEmail('autre.agent@example.gouv.fr')

    expect(wrapper.emitted('reset')).toHaveLength(1)
    wrapper.unmount()
  })

  it('surfaces a conflict on the email field', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()
    wrapper.vm.setEmailError('Cet agent est déjà rattaché à l\'organisme.')
    await nextTick()

    expect(document.body.textContent).toContain('Cet agent est déjà rattaché')
    wrapper.unmount()
  })
})
