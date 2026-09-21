import type { AgentRecherche } from '@/features/organismes/types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import AssignationResponsableDrawer from './AssignationResponsableDrawer.vue'

const EMAIL = 'jeanne.dupont@example.gouv.fr'

const AGENT: AgentRecherche = {
  agent_id: 'bbbbbbbb-0001-0001-0001-000000000001',
  email: EMAIL,
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Chargée de recrutement',
}

const RECRUTEMENTS = RECRUTEMENTS_ACTIFS.slice(0, 2)

function mountDrawer(props: Record<string, unknown> = {}) {
  return mount(AssignationResponsableDrawer, {
    props: {
      open: true,
      recrutements: RECRUTEMENTS,
      status: 'idle',
      ...props,
    },
    attachTo: document.body,
  })
}

function submitButton() {
  return document.querySelector<HTMLButtonElement>('button[type="submit"]')!
}

function dismissButtons() {
  return [...document.querySelectorAll<HTMLButtonElement>('.csp-tag--dismissible')]
}

describe('assignationResponsableDrawer', () => {
  it('assigns the agent found for that email', async () => {
    const wrapper = mountDrawer({ status: 'found', agent: AGENT })
    await nextTick()

    expect(document.body.textContent).toContain('Jeanne Dupont')
    expect(submitButton().textContent).toContain('Assigner un responsable')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('assign')).toEqual([[]])
    wrapper.unmount()
  })

  it('announces the account creation when no agent matches the email', async () => {
    const wrapper = mountDrawer({ status: 'not-found' })
    await nextTick()

    expect(document.body.textContent).toContain('Un compte sera créé')
    expect(submitButton().textContent).toContain('Créer et assigner')
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('assign')).toEqual([[]])
    wrapper.unmount()
  })

  it('shows one dismissible tag per selected offer', async () => {
    const wrapper = mountDrawer()
    await nextTick()

    expect(dismissButtons().map(button => button.textContent?.trim())).toEqual(
      RECRUTEMENTS.map(recrutement => recrutement.intitule),
    )
    expect(document.body.textContent).toContain('2 offres sélectionnées')
    wrapper.unmount()
  })

  it('asks to remove the offer whose tag is dismissed', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    dismissButtons()[1].click()
    await nextTick()

    expect(wrapper.emitted('remove')).toEqual([[RECRUTEMENTS[1].offer_id]])
    wrapper.unmount()
  })

  it('closes itself once every offer has been removed', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await wrapper.setProps({ recrutements: [] })

    expect(wrapper.emitted('update:open')).toEqual([[false]])
    wrapper.unmount()
  })
})
