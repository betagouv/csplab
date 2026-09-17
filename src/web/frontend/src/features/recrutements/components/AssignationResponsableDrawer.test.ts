import type { AgentOrganisme } from '@/features/organismes/types'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { nextTick } from 'vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import AssignationResponsableDrawer from './AssignationResponsableDrawer.vue'

const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'

const AGENTS: AgentOrganisme[] = [
  {
    agent_id: AGENT_ID,
    organisme_id: '11111111-1111-1111-1111-111111111111',
    nom: 'Dupont',
    prenom: 'Jeanne',
    email: 'jeanne.dupont@example.gouv.fr',
    poste: 'Chargée de recrutement',
    role: 'agent',
    date_derniere_activite: null,
    date_creation_compte: '2026-01-01T00:00:00Z',
  },
]

const RECRUTEMENTS = RECRUTEMENTS_ACTIFS.slice(0, 2)

function mountDrawer(props: Record<string, unknown> = {}) {
  return mount(AssignationResponsableDrawer, {
    props: {
      open: true,
      recrutements: RECRUTEMENTS,
      agents: AGENTS,
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

async function pickAgent(wrapper: ReturnType<typeof mountDrawer>, agentId: string) {
  wrapper.findComponent(CspCombobox).vm.$emit('update:modelValue', agentId)
  await nextTick()
}

describe('assignationResponsableDrawer', () => {
  it('assigns the selected agent to the selected offers', async () => {
    const wrapper = mountDrawer()
    await nextTick()
    await pickAgent(wrapper, AGENT_ID)
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('assign')).toEqual([[AGENT_ID]])
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

  it('does not assign anybody while no agent is selected', async () => {
    const wrapper = mountDrawer()
    await nextTick()

    expect(submitButton().disabled).toBe(true)
    submitButton().click()
    await nextTick()

    expect(wrapper.emitted('assign')).toBeUndefined()
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
